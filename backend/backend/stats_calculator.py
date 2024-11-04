import time
import math
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R

from backend.database import Database  # Pour convertir les quaternions en matrices de rotation
from django.utils import timezone

from head_memory.models import HeadMemory
from chest_memory.models import ChestMemory
from left_leg_memory.models import LeftLegMemory
from right_leg_memory.models import RightLegMemory


MEMORY_MODELS = {
    'BNO055_head': HeadMemory,
    'BNO055_chest': ChestMemory,
    'BNO055_left_leg': LeftLegMemory,
    'BNO055_right_leg': RightLegMemory,
}

def quaternion_to_euler(w, x, y, z):
    """
    Convertit un quaternion en angles d'Euler (en degrés).
    """
    # Normalisation du quaternion
    
    norm = np.sqrt(w*w + x*x + y*y + z*z)
    if (w != 0) : w /= norm
    if (x != 0) : x /= norm
    if (y != 0) : y /= norm
    if (z != 0) : z /= norm

    # Calcul des angles d'Euler
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = np.arctan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = np.clip(t2, -1.0, +1.0)
    pitch_y = np.arcsin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = np.arctan2(t3, t4)

    # Conversion en degrés
    roll_x = np.degrees(roll_x)
    pitch_y = np.degrees(pitch_y)
    yaw_z = np.degrees(yaw_z)

    return roll_x, pitch_y, yaw_z

class BNO05Sensor:
    def __init__(self, name, db_connection, initial_position, session_id):
        self.db = db_connection  # db_connection est une instance de Database
        self.name = name
        self.session_id = session_id
        
        MEMORY_NAME = {
            'BNO055_head': 'BNO055_head_memory',
            'BNO055_chest': 'BNO055_chest_memory',
            'BNO055_left_leg': 'BNO055_left_leg_memory',
            'BNO055_right_leg': 'BNO055_right_leg_memory',
        }

        memory_data = self.db.to_dataframe_id(MEMORY_NAME.get(self.name), self.session_id)
        
        try:
            self.g_measurements = memory_data['g_measurement'].tolist() if not memory_data['g_measurement'].empty else [0]
            self.velocities_norm = memory_data['velocity_norm'].tolist() if not memory_data['velocity_norm'].empty else [0]
            self.distance = memory_data['distance'].iloc[-1] if not memory_data['distance'].empty else 0
        except KeyError as e:
            print(f"Column missing in memory data: {e}")
            self.g_measurements = [0]
            self.velocities_norm = [0]
            self.distance = 0

        self.data = pd.DataFrame()  # Initialisation de self.data
        self.update_data()  # Récupérer les dernières données

        # Initialisation de self.df
        transformed_data = self.db.to_dataframe_id(self.name + '_transformed', self.session_id)
        
        if transformed_data.empty:
            self.df = pd.DataFrame({
                'session_id': [self.session_id],
                'timestamp': [timezone.now()],
                'accel_x': [0],
                'accel_y': [0],
                'accel_z': [0],
                'vel_x': [0],
                'vel_y': [0],
                'vel_z': [0],
                'pos_x': [initial_position[0]],
                'pos_y': [initial_position[1]],
                'pos_z': [initial_position[2]]
            })
        else:
            self.df = transformed_data
            
    def update_data(self):
        # Récupérer dynamiquement les dernières données pour la session active depuis la base de données
        try:
            self.data = self.db.to_dataframe_id(self.name, self.session_id)
            if self.data.empty:
                # print(f"Aucune donnée reçue pour {self.name}. Étape de calcul ignorée.")
                a = 0
            else:
                # Convertir la colonne 'time' en datetime
                self.data['time'] = pd.to_datetime(self.data['time'])
        except Exception as e:
            print(f"Erreur lors de la récupération des données pour {self.name}: {e}")
            self.data = pd.DataFrame()

    def check_session(self):
        if self.session_id is not None:
            count = len(self.data)
            return count
        else:
            return 0

    def dt(self):
        if self.check_session() < 2:
            return 0.5
        last_timestamp = self.data.iloc[-1]['time']
        previous_timestamp = self.data.iloc[-2]['time']
        dt = (last_timestamp - previous_timestamp).total_seconds()
        return dt if dt > 0 else 0.5

    def integration(self):
        self.update_data()
        if self.check_session() > 0:
            # Calcul de l'accélération
            accel_x = self.data.iloc[-1]["accel_x"]
            accel_y = self.data.iloc[-1]["accel_y"]
            accel_z = self.data.iloc[-1]["accel_z"]

            # Conversion du quaternion en matrice de rotation
            if not (self.data.iloc[-1]['quat_w'] == 0 and self.data.iloc[-1]['quat_x'] == 0 and self.data.iloc[-1]['quat_y'] == 0 and self.data.iloc[-1]['quat_z'] == 0):
                rotation_matrix = R.from_quat([
                    self.data.iloc[-1]['quat_x'],
                    self.data.iloc[-1]['quat_y'],
                    self.data.iloc[-1]['quat_z'],
                    self.data.iloc[-1]['quat_w']
                ]).as_matrix()
            else:
                print("Quaternion values are all zero, skipping rotation matrix calculation.")
                return self.df

            local_acceleration = np.array([accel_x, accel_y, accel_z])
            global_acceleration = np.dot(rotation_matrix.T, local_acceleration)

            self.g_measurements.append(np.linalg.norm(global_acceleration) / 9.81)  # Norme de l'accélération

            # Calcul de la vitesse
            velocity = self.df.iloc[-1][['vel_x', 'vel_y', 'vel_z']].values + global_acceleration * self.dt()
            velocity_norm = np.linalg.norm(velocity)
            self.velocities_norm.append(velocity_norm)

            # Calcul de la position
            if self.df.shape[0] > 1:
                previous_position = self.df.iloc[-1][['pos_x', 'pos_y', 'pos_z']].values
            else:
                previous_position = np.array([self.df.iloc[-1]['pos_x'], self.df.iloc[-1]['pos_y'], self.df.iloc[-1]['pos_z']])

            position = previous_position + velocity * self.dt()

            # Créer un DataFrame pour la nouvelle ligne à ajouter
            new_data = pd.DataFrame({
                'session_id': [self.session_id],
                'timestamp': [self.data.iloc[-1]['time']],
                'accel_x': [global_acceleration[0]],
                'accel_y': [global_acceleration[1]],
                'accel_z': [global_acceleration[2]],
                'vel_x': [velocity[0]],
                'vel_y': [velocity[1]],
                'vel_z': [velocity[2]],
                'pos_x': [position[0]],
                'pos_y': [position[1]],
                'pos_z': [position[2]]
            })
            
            self.df = pd.concat([self.df, new_data], ignore_index=True)
            
            memory_model = MEMORY_MODELS.get(self.name)
            if memory_model:
                memory_model.objects.create(
                    session_id_id=self.session_id,
                    time=timezone.now(),
                    g_measurement=self.g_measurements[-1],
                    distance=self.distance,
                    velocity_norm=self.velocities_norm[-1]
                )
        
            return self.df
        else:
            return self.df

    def compute_g(self):
        return self.g_measurements[-1]
    
    

    def pace(self, window_size=10):
        if len(self.velocities_norm) < window_size:
            pace = 0
        else:
            pace = np.mean(self.velocities_norm[-window_size:])
        pace_km_per_hour = pace * 3.6
        return pace_km_per_hour

    def compute_distance(self):
        if len(self.df) > 1:
            pos_prev = self.df.iloc[-2][['pos_x', 'pos_y', 'pos_z']].to_numpy()
            pos_curr = self.df.iloc[-1][['pos_x', 'pos_y', 'pos_z']].to_numpy()
            delta_position = abs(np.linalg.norm(pos_curr - pos_prev))
            self.distance += delta_position
        return self.distance

# Définition des classes des capteurs avec corrections
class HeadSensor(BNO05Sensor):
    def __init__(self, db_connection, session_id, player_height=1.80):
        initial_position = (player_height * 0.97, 0, 0)
        super().__init__('BNO055_head', db_connection, initial_position, session_id)

    def get_euler_angles(self):
        # Récupérer les quaternions depuis la base de données
        df = self.db.to_dataframe_id('BNO055_head', self.session_id)[['quat_w', 'quat_x', 'quat_y', 'quat_z']]

        # Appliquer la conversion
        euler_angles = df.apply(lambda row: quaternion_to_euler(row['quat_w'], row['quat_x'], row['quat_y'], row['quat_z']), axis=1)
        euler_df = pd.DataFrame(euler_angles.tolist(), columns=['roll', 'pitch', 'yaw'])

        # Fusionner avec le DataFrame initial si nécessaire
        return euler_df

class ChestSensor(BNO05Sensor):
    def __init__(self, db_connection, session_id, player_height=1.80):
        initial_position = (player_height * 0.60, 0, 0)
        super().__init__('BNO055_chest', db_connection, initial_position, session_id)

    def get_euler_angles(self):
        # Récupérer les quaternions depuis la base de données
        df = self.db.to_dataframe_id('BNO055_chest', self.session_id)[['quat_w', 'quat_x', 'quat_y', 'quat_z']]

        # Appliquer la conversion
        euler_angles = df.apply(lambda row: quaternion_to_euler(row['quat_w'], row['quat_x'], row['quat_y'], row['quat_z']), axis=1)
        euler_df = pd.DataFrame(euler_angles.tolist(), columns=['roll', 'pitch', 'yaw'])

        # Fusionner avec le DataFrame initial si nécessaire
        return euler_df

class RightLegSensor(BNO05Sensor):
    def __init__(self, db_connection, session_id, player_height=1.80, player_width=0.4):
        initial_position = (player_height * 0.33, player_width * 0.20, 0)
        super().__init__('BNO055_right_leg', db_connection, initial_position, session_id)

class LeftLegSensor(BNO05Sensor):
    def __init__(self, db_connection, session_id, player_height=1.80, player_width=0.4):
        initial_position = (player_height * 0.33, -player_width * 0.20, 0)
        super().__init__('BNO055_left_leg', db_connection, initial_position, session_id)



# Classe pour les statistiques en temps réel
class RealTimeStatistics:
    def __init__(self, db: Database, session_id):
        self.db = db
        self.active_session_id = session_id  # db_connection est une instance de Database

        self.head_sensor = HeadSensor(self.db, session_id=self.active_session_id)
        self.chest_sensor = ChestSensor(self.db, session_id=self.active_session_id)
        self.right_leg_sensor = RightLegSensor(self.db, session_id=self.active_session_id)
        self.left_leg_sensor = LeftLegSensor(self.db, session_id=self.active_session_id)

        # Lire les données BMP280 et MAX30102 depuis la base de données
        self.BMP280 = self.db.to_dataframe_id('BMP280', self.active_session_id)
        self.MAX30102 = self.db.to_dataframe_id('MAX30102', self.active_session_id)

    def start_timer(self):
        start_time = self.sessions.loc[self.sessions['session_id'] == self.active_session_id, 'start_time'].values[0]
        start_time = pd.to_datetime(start_time)
        try:
            while self.active_session_id is not None:
                elapsed_time = (pd.Timestamp.now() - start_time).total_seconds()
                # print(f'Temps écoulé : {elapsed_time:.2f} secondes', end='\r')
                time.sleep(0.1)
        except KeyboardInterrupt:
            print('\nTimer stopped.')

    def get_BNO_data(self, sensor_name):
        if sensor_name == 'BNO055_head':
            return self.head_sensor.integration()  # Mise à jour en temps réel
        elif sensor_name == 'BNO055_chest':
            return self.chest_sensor.integration()
        elif sensor_name == 'BNO055_right_leg':
            return self.right_leg_sensor.integration()
        elif sensor_name == 'BNO055_left_leg':
            return self.left_leg_sensor.integration()
        else:
            print(f"Capteur {sensor_name} non reconnu.")
            return None

    def get_BNO_g(self, sensor_name):
        if sensor_name == 'BNO055_head':
            return self.head_sensor.compute_g()
        elif sensor_name == 'BNO055_chest':
            return self.chest_sensor.compute_g()
        elif sensor_name == 'BNO055_right_leg':
            return self.right_leg_sensor.compute_g()
        elif sensor_name == 'BNO055_left_leg':
            return self.left_leg_sensor.compute_g()
        else:
            print(f"Capteur {sensor_name} non reconnu.")
            return None

    def get_BNO_pace(self, sensor_name):
        if sensor_name == 'BNO055_head':
            return self.head_sensor.pace()
        elif sensor_name == 'BNO055_chest':
            return self.chest_sensor.pace()
        elif sensor_name == 'BNO055_right_leg':
            return self.right_leg_sensor.pace()
        elif sensor_name == 'BNO055_left_leg':
            return self.left_leg_sensor.pace()
        else:
            print(f"Capteur {sensor_name} non reconnu.")
            return None

    def get_BNO_distance(self, sensor_name):
        if sensor_name == 'BNO055_head':
            return self.head_sensor.compute_distance()
        elif sensor_name == 'BNO055_chest':
            print("distance chest :" , self.chest_sensor.compute_distance())
            return self.chest_sensor.compute_distance()
        elif sensor_name == 'BNO055_right_leg':
            return self.right_leg_sensor.compute_distance()
        elif sensor_name == 'BNO055_left_leg':
            return self.left_leg_sensor.compute_distance()
        else:
            print(f"Capteur {sensor_name} non reconnu.")
            return None
    
    def max_g(self): 
        head_max_g = max(self.head_sensor.g_measurements, default=0)
        chest_max_g = max(self.chest_sensor.g_measurements, default=0)

        max_g = max(head_max_g, chest_max_g)

        print(f"Max G measured: {max_g}")
        return max_g

    def relative_position(self, BNO_1, BNO_2):
        df1 = self.get_BNO_data(BNO_1)
        df2 = self.get_BNO_data(BNO_2)

        if df1 is not None and df2 is not None:
            pos1 = df1[['pos_x', 'pos_y', 'pos_z']].iloc[-1].to_numpy()
            pos2 = df2[['pos_x', 'pos_y', 'pos_z']].iloc[-1].to_numpy()

            relative_pos = pos2 - pos1
            return relative_pos
        else:
            # print("Impossible de calculer la position relative.")
            return None

    def temperature(self):
        if not self.BMP280.empty:
            return self.BMP280.iloc[-1]["temperature"]
        else:
            # print("No BMP280 data available.")
            return None

    def pressure(self):
        if not self.BMP280.empty:
            return self.BMP280.iloc[-1]["pressure"]
        else:
            # print("No BMP280 data available.")
            return None

    def BPM(self):
        if not self.MAX30102.empty:
            return self.MAX30102.iloc[-1]["BPM"]
        else:
            # print("No MAX30102 data available.")
            return None

    def SpO2(self):
        if not self.MAX30102.empty:
            return self.MAX30102.iloc[-1]["SpO2"]
        else:
            # print("No MAX30102 data available.")
            return None

class ShockAlert:
    def __init__(self, threshold_g=20):
        self.threshold_g = threshold_g
        # print(f"ShockAlert initialized with threshold: {self.threshold_g}G")

    def check_shock(self, dataframe):
        """
        Check if a shock exceeds the threshold and returns a message with sensor data.
        :param dataframe: pandas DataFrame containing 'accel_x', 'accel_y', 'accel_z' columns.
        :return: List of messages with all sensor data if shock > threshold_g.
        """
        messages = []
        for index, row in dataframe.iterrows():
            acc_x, acc_y, acc_z = row['accel_x'], row['accel_y'], row['accel_z']
            total_acc = np.sqrt(acc_x**2 + acc_y**2 + acc_z**2)
            # print(f"Total acceleration at index {index}: {total_acc:.2f}G")

            if total_acc > self.threshold_g:
                messages.append(f"Shock detected: {total_acc:.2f}G at index {index}.\nSensor data: {row.to_dict()}")

        if messages:
            print(f"Shock alerts generated: {len(messages)}")
        else:
            print("No shocks detected.")
        return messages if messages else None

class FatigueCalculator:
    def __init__(self, db, session_id, max_bpm=200, normal_inclination=15, fatigue_factor=0.5):
        self.session_id = session_id
        self.max_bpm = max_bpm
        self.normal_inclination = normal_inclination  # Seuil normal d'inclinaison en degrés
        self.fatigue_factor = fatigue_factor  # Pourcentage de fatigue supplémentaire par degré d'inclinaison
        self.db = db

    def calculate_fatigue(self):
        # Récupérer les données de fréquence cardiaque et filtrer les BPM invalides (BPM = 0)
        heart_rate_df = self.db.to_dataframe('MAX30102')
        heart_rate_df = heart_rate_df[heart_rate_df['BPM'] > 0].reset_index(drop=True)

        # Récupérer les quaternions pour la tête et la poitrine
        head_df = self.db.to_dataframe('BNO055_head')[['quat_w', 'quat_x', 'quat_y', 'quat_z']]
        chest_df = self.db.to_dataframe('BNO055_chest')[['quat_w', 'quat_x', 'quat_y', 'quat_z']]

        # Convertir les quaternions en angles d'Euler pour la tête
        head_euler_df = head_df.apply(lambda row: quaternion_to_euler(row['quat_w'], row['quat_x'], row['quat_y'], row['quat_z']), axis=1, result_type='expand')
        head_euler_df.columns = ['roll', 'pitch', 'yaw']

        # Convertir les quaternions en angles d'Euler pour la poitrine
        chest_euler_df = chest_df.apply(lambda row: quaternion_to_euler(row['quat_w'], row['quat_x'], row['quat_y'], row['quat_z']), axis=1, result_type='expand')
        chest_euler_df.columns = ['roll', 'pitch', 'yaw']

        # Synchroniser les DataFrames en fonction de la longueur minimale
        min_length = min(len(heart_rate_df), len(head_euler_df), len(chest_euler_df))
        heart_rate_df = heart_rate_df.iloc[:min_length].reset_index(drop=True)
        head_euler_df = head_euler_df.iloc[:min_length].reset_index(drop=True)
        chest_euler_df = chest_euler_df.iloc[:min_length].reset_index(drop=True)

        # Calculer les différences d'angles
        delta_roll = head_euler_df['roll'] - chest_euler_df['roll']
        delta_pitch = head_euler_df['pitch'] - chest_euler_df['pitch']
        delta_yaw = head_euler_df['yaw'] - chest_euler_df['yaw']

        # Calculer l'inclinaison totale
        inclination_angle = np.sqrt(delta_roll**2 + delta_pitch**2 + delta_yaw**2)

        fatigue_list = []
        for index in heart_rate_df.index:
            bpm = heart_rate_df.at[index, 'BPM']

            # Calcul de la fatigue de base
            base_fatigue = (bpm / self.max_bpm) * 100
            base_fatigue = min(base_fatigue, 100)

            # Calcul de la fatigue supplémentaire basée sur l'inclinaison
            if inclination_angle[index] > self.normal_inclination:
                extra_fatigue = (inclination_angle[index] - self.normal_inclination) * self.fatigue_factor
            else:
                extra_fatigue = 0

            total_fatigue = base_fatigue + extra_fatigue
            total_fatigue = min(total_fatigue, 100)
            fatigue_list.append(total_fatigue)

            # print(f"BPM: {bpm}, Base Fatigue: {base_fatigue:.2f}%, Inclination Angle: {inclination_angle[index]:.2f}°, Extra Fatigue: {extra_fatigue:.2f}%, Total Fatigue: {total_fatigue:.2f}%")

        average_fatigue = np.mean(fatigue_list)
        # print(f"Fatigue moyenne ajustée : {average_fatigue:.2f}%")
        return average_fatigue

class PostTrainingAnalysis:
    def __init__(self, db_connection):
        self.db = db_connection  # db_connection est une instance de Database
        self.total_bpm = 0
        self.bpm_count = 0
        self.shock_count = 0
        self.shock_threshold = 20
        self.rest_days = 0
        self.running_threshold = 15  # Seuil d'accélération pour considérer que le joueur court
        self.running_time = 0  # Temps pendant lequel le joueur court
        self.standing_time = 0  # Temps pendant lequel le joueur est presque sur place
        # print("PostTrainingAnalysis initialized.")

    def get_chest_data(self, session_id):
        """
        Récupère les données du capteur BNO055 situé sur la poitrine pour un session_id donné.
        :param session_id: Identifiant de la session d'entraînement.
        :return: DataFrame des données de capteurs (accélération).
        """
        df = self.db.to_dataframe_id('BNO055_chest', session_id)
        if not df.empty:
            # print(f"Retrieved chest data for session {session_id}: {len(df)} entries.")
            return df[['accel_x', 'accel_y', 'accel_z']]
        else:
            # print(f"No chest data found for session {session_id}.")
            return pd.DataFrame(columns=['accel_x', 'accel_y', 'accel_z'])

    def analyze(self, session_id):
        """
        Effectue l'analyse post-entrainement basée sur les données du capteur BNO055_chest.
        :param session_id: Identifiant de la session d'entraînement.
        :return: Dictionnaire avec risque de concussion, intensité d'entraînement et jours de repos recommandés.
        """
        session_data = self.get_chest_data(session_id)
        total_time = len(session_data) * 0.5  # Supposons que chaque mesure est prise toutes les 0,5 secondes
        # print(f"Total analysis time for session {session_id}: {total_time:.2f} seconds.")

        for index, row in session_data.iterrows():
            acc_x, acc_y, acc_z = row['accel_x'], row['accel_y'], row['accel_z']
            total_acc = np.sqrt(acc_x**2 + acc_y**2 + acc_z**2)

            # Analyse des chocs
            if total_acc > self.shock_threshold:
                self.shock_count += 1
                # print(f"Shock detected! Total acceleration: {total_acc:.2f}G")
                if total_acc > 50:  # Seuil de choc violent
                    self.rest_days += 3
                    # print("Severe shock detected. Adding 3 days of rest.")

            # Déterminer le temps de course ou de stationnement
            if total_acc > self.running_threshold:
                self.running_time += 0.5  # Le joueur est considéré comme courant
            else:
                self.standing_time += 0.5  # Le joueur est considéré comme immobile ou presque

        # Calculer l'intensité de l'entraînement
        intensity = (self.running_time / total_time) * 100 if total_time > 0 else 0
        # print(f"Training intensity: {intensity:.2f}%")

        # Détermination du risque de concussion
        concussion_risk = min(self.shock_count, 5)  # Échelle de risque de 0 à 5
        # print(f"Concussion risk level: {concussion_risk}")

        return {
            'concussion_risk': concussion_risk,
            'training_intensity': intensity,
            'number_of_shocks': self.shock_count,
            'recommended_rest_days': self.rest_days
        }

class FootingQuality:
    def __init__(self, db_connection, session_id):
        self.db = db_connection
        self.session_id = session_id
        self.left_leg_sensor = LeftLegSensor(self.db, session_id)
        self.right_leg_sensor = RightLegSensor(self.db, session_id)
        self.chest_sensor = ChestSensor(self.db, session_id)
        self.head_sensor = HeadSensor(self.db, session_id)

    def calculate_stance_width(self):
        left_leg_data = self.left_leg_sensor.integration()
        right_leg_data = self.right_leg_sensor.integration()

        if left_leg_data.empty or right_leg_data.empty:
            # print("Données insuffisantes pour calculer l'écartement.")
            return 0.0

        left_position = left_leg_data[['pos_x', 'pos_y', 'pos_z']].iloc[-1].values
        right_position = right_leg_data[['pos_x', 'pos_y', 'pos_z']].iloc[-1].values
        width = np.linalg.norm(left_position - right_position)

        # Normalisation
        typical_stance_width = 3000  # Valeur typique ajustée
        normalized_stance = max(0.0, min(width / typical_stance_width, 1.0))
        # print(f"Écartement calculé: {width:.2f}, Normalisé: {normalized_stance:.2f}")

        return normalized_stance

    def calculate_stability(self):
        left_leg_data = self.left_leg_sensor.integration()
        right_leg_data = self.right_leg_sensor.integration()

        # Utilisation des dernières valeurs d'accélération
        left_accel = left_leg_data[['accel_x', 'accel_y', 'accel_z']]
        right_accel = right_leg_data[['accel_x', 'accel_y', 'accel_z']]

        # Calcul de la norme de l'accélération pour chaque capteur
        left_accel_magnitudes = np.linalg.norm(left_accel.values, axis=1)
        right_accel_magnitudes = np.linalg.norm(right_accel.values, axis=1)

        # Calcul des moyennes des magnitudes d'accélération
        left_avg_accel = np.mean(left_accel_magnitudes) if len(left_accel_magnitudes) > 0 else 0
        right_avg_accel = np.mean(right_accel_magnitudes) if len(right_accel_magnitudes) > 0 else 0

        # Seuil de tolérance pour une bonne stabilité
        stability_threshold = 9.81  # Valeur en m/s² (accélération due à la gravité)

        # Calcul de la stabilité
        left_stability = max(0.0, 1 - abs(left_avg_accel - stability_threshold) / stability_threshold)
        right_stability = max(0.0, 1 - abs(right_avg_accel - stability_threshold) / stability_threshold)

        # Moyenne des scores de stabilité des deux jambes
        stability_score = (left_stability + right_stability) / 2

        # print(f"Stabilité calculée: Left: {left_stability:.2f}, Right: {right_stability:.2f}, Score: {stability_score:.2f}")
        return stability_score


    def calculate_alignment(self):
        chest_data = self.chest_sensor.integration()
        head_data = self.head_sensor.integration()

        if chest_data.empty or head_data.empty:
            # print("Données insuffisantes pour calculer l'alignement.")
            return 0.0

        chest_position = chest_data[['pos_x', 'pos_y', 'pos_z']].iloc[-1].values
        head_position = head_data[['pos_x', 'pos_y', 'pos_z']].iloc[-1].values
        alignment_vector = head_position - chest_position

        # Normalisation
        typical_alignment_tolerance = 1000
        alignment_score = max(0.0, 1 - (np.abs(alignment_vector[1]) / typical_alignment_tolerance))

        # print(f"Alignement calculé (écart en y): {alignment_vector[1]:.2f}, Normalisé: {alignment_score:.2f}")
        return alignment_score

    def footing_quality_score(self):
        stance_width = self.calculate_stance_width()
        stability = self.calculate_stability()
        alignment = self.calculate_alignment()

        stance_weight = 0.3
        stability_weight = 0.4
        alignment_weight = 0.3

        quality_score = (stance_width * stance_weight +
                         stability * stability_weight +
                         alignment * alignment_weight)

        # print(f"Score de qualité des appuis calculé: {quality_score:.2f}")
        return quality_score