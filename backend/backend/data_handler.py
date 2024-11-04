# Fichier pour gérer l'arrivée de data depuis le broker


import threading
from backend.database import Database
from datetime import datetime
import sqlite3
from backend.stats_calculator import *
from django.conf import settings
from head.models import Head
from head_transformed.models import HeadTransformed
from chest.models import Chest
from chest_transformed.models import ChestTransformed
from right_leg.models import RightLeg
from right_leg_transformed.models import RightLegTransformed
from left_leg.models import LeftLeg
from left_leg_transformed.models import LeftLegTransformed
from heart_rate.models import HeartRate
from temperature.models import Temperature
from concussion_stats.models import ConcussionStats
from session_stats.models import SessionStats

from session.models import Session
from django.utils.timezone import make_aware
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async, async_to_sync
from django.utils.timezone import make_aware, is_naive

def serialize_data(data):
    """Convertit les objets datetime en chaînes de caractères dans les dictionnaires de données."""
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()  # Convertit en format ISO
        elif isinstance(value, dict):
            serialize_data(value)  # Appel récursif pour les sous-dictionnaires
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    serialize_data(item)  # Conversion dans les éléments de la liste
    return data


class DataHandler:
    def __init__(self, db):
        self.db = db
        self.connection = self.db.connection
        self.cursor = self.db.connection.cursor()
        self.active_session_id = None
        self.pause_session = False
        self.lock = threading.Lock()  # Verrou pour accès concurrent à la base        
        self.channel_layer = get_channel_layer()



    def get_last_session_id(self):
        if self.db.check_table_exists("training_sessions") == True : 
            self.cursor.execute('''
                SELECT MAX(session_id) FROM training_sessions
            ''')
            last_session_id = self.cursor.fetchone()[0]
            if last_session_id is None :
                return 0
            return last_session_id
        return 0
    
    async def get_all_data(self):
        # Récupère toutes les données de chaque table
        data = {
            "head_data": await sync_to_async(list)(Head.objects.values()),
            "head_transformed_data": await sync_to_async(list)(HeadTransformed.objects.values()),
            "chest_data": await sync_to_async(list)(Chest.objects.values()),
            "chest_transformed_data": await sync_to_async(list)(ChestTransformed.objects.values()),
            "right_leg_data": await sync_to_async(list)(RightLeg.objects.values()),
            "right_leg_transformed_data": await sync_to_async(list)(RightLegTransformed.objects.values()),
            "left_leg_data": await sync_to_async(list)(LeftLeg.objects.values()),
            "left_leg_transformed_data": await sync_to_async(list)(LeftLegTransformed.objects.values()),
            "heart_rate_data": await sync_to_async(list)(HeartRate.objects.values()),
            "temperature_data": await sync_to_async(list)(Temperature.objects.values()),
            "concussion_stats_data": await sync_to_async(list)(ConcussionStats.objects.values()),
            "session_stats_data": await sync_to_async(list)(SessionStats.objects.values()),
        }
        # Appelle la fonction de sérialisation pour convertir les datetime en chaînes de caractères
        return serialize_data(data)

    
    async def send_data_via_websocket(self):
        # Envoie toutes les données au WebSocket de manière asynchrone
        data = await self.get_all_data()  # Appel asynchrone de get_all_data
        await self.channel_layer.group_send(
            "data_group",
            {
                "type": "send_data",
                "data": data,
            }
        )

        
    def process_data(self, data):
        if self.active_session_id is not None :          
            time_now = timezone.now()
            
            with self.lock:  # Utilisation du verrou lors de l'accès à la base
                print(f"Inserting measures for session {self.get_last_session_id()}")
                session = Session.objects.get(session_id=self.active_session_id)

                if 'MAX30102' in data :                  
                    HeartRate.objects.create(
                        session_id=session,
                        time=time_now,
                        SpO2=data['MAX30102']["SpO2"],
                        BPM=data['MAX30102']['BPM']
                    )
                if 'BMP280' in data :
                    Temperature.objects.create(
                        session_id=session,
                        time=time_now,
                        temperature=data['BMP280']["temperature"],
                        pressure=data['BMP280']['pressure']
                    )               
                if 'BNO055_head' in data :
                    Head.objects.create(
                        session_id=session,
                        time=time_now,
                        accel_x=data['BNO055_head']["accel_x"],
                        accel_y=data['BNO055_head']['accel_y'],
                        accel_z=data['BNO055_head']["accel_z"],
                        quat_w=data['BNO055_head']["quat_w"],
                        quat_x=data['BNO055_head']["quat_x"],
                        quat_y=data['BNO055_head']['quat_y'],
                        quat_z=data['BNO055_head']["quat_z"]
                    )
                    
                    head_df = HeadSensor(self.db, self.active_session_id).integration() 
                                       
                    timestamp = head_df.iloc[-1]['timestamp']
                    # if is_naive(timestamp):
                    #     timestamp = make_aware(timestamp)
                        
                    HeadTransformed.objects.create(
                        session_id=session,
                        timestamp=make_aware(head_df.iloc[-1]['timestamp']),
                        accel_x=head_df.iloc[-1]['accel_x'],
                        accel_y=head_df.iloc[-1]['accel_y'],
                        accel_z=head_df.iloc[-1]['accel_z'],
                        vel_x=head_df.iloc[-1]['vel_x'],
                        vel_y=head_df.iloc[-1]['vel_y'],
                        vel_z=head_df.iloc[-1]['vel_z'],
                        pos_x=head_df.iloc[-1]['pos_x'],
                        pos_y=head_df.iloc[-1]['pos_y'],
                        pos_z=head_df.iloc[-1]['pos_z']
                    )
                if 'BNO055_chest' in data :
                    Chest.objects.create(
                        session_id=session,
                        time=time_now,
                        accel_x=data['BNO055_chest']["accel_x"],
                        accel_y=data['BNO055_chest']['accel_y'],
                        accel_z=data['BNO055_chest']["accel_z"],
                        quat_w=data['BNO055_chest']["quat_w"],
                        quat_x=data['BNO055_chest']["quat_x"],
                        quat_y=data['BNO055_chest']['quat_y'],
                        quat_z=data['BNO055_chest']["quat_z"]
                    )
                    chest_df = ChestSensor(self.db, self.active_session_id).integration()
                    
                    timestamp = chest_df.iloc[-1]['timestamp']
                    # if is_naive(timestamp):
                    #     timestamp = make_aware(timestamp)
                        
                    ChestTransformed.objects.create(
                        session_id=session,
                        timestamp=timestamp,
                        accel_x=chest_df.iloc[-1]['accel_x'],
                        accel_y=chest_df.iloc[-1]['accel_y'],
                        accel_z=chest_df.iloc[-1]['accel_z'],
                        vel_x=chest_df.iloc[-1]['vel_x'],
                        vel_y=chest_df.iloc[-1]['vel_y'],
                        vel_z=chest_df.iloc[-1]['vel_z'],
                        pos_x=chest_df.iloc[-1]['pos_x'],
                        pos_y=chest_df.iloc[-1]['pos_y'],
                        pos_z=chest_df.iloc[-1]['pos_z']
                    )
                if 'BNO055_right_leg' in data :
                    RightLeg.objects.create(
                        session_id=session,
                        time=time_now,
                        accel_x=data['BNO055_right_leg']["accel_x"],
                        accel_y=data['BNO055_right_leg']['accel_y'],
                        accel_z=data['BNO055_right_leg']["accel_z"],
                        quat_w=data['BNO055_right_leg']["quat_w"],
                        quat_x=data['BNO055_right_leg']["quat_x"],
                        quat_y=data['BNO055_right_leg']['quat_y'],
                        quat_z=data['BNO055_right_leg']["quat_z"]
                    )          
                    right_leg_df = RightLegSensor(self.db, self.active_session_id).integration()
                    
                    timestamp = right_leg_df.iloc[-1]['timestamp']
                    # if is_naive(timestamp):
                    #     timestamp = make_aware(timestamp)
                        
                    RightLegTransformed.objects.create(
                        session_id=session,
                        timestamp=timestamp,
                        accel_x=right_leg_df.iloc[-1]['accel_x'],
                        accel_y=right_leg_df.iloc[-1]['accel_y'],
                        accel_z=right_leg_df.iloc[-1]['accel_z'],  
                        vel_x=right_leg_df.iloc[-1]['vel_x'],
                        vel_y=right_leg_df.iloc[-1]['vel_y'],
                        vel_z=right_leg_df.iloc[-1]['vel_z'],
                        pos_x=right_leg_df.iloc[-1]['pos_x'],
                        pos_y=right_leg_df.iloc[-1]['pos_y'],
                        pos_z=right_leg_df.iloc[-1]['pos_z']
                    )
                if 'BNO055_left_leg' in data :
                    LeftLeg.objects.create(
                        session_id=session,
                        time=time_now,
                        accel_x=data['BNO055_left_leg']["accel_x"],
                        accel_y=data['BNO055_left_leg']['accel_y'],
                        accel_z=data['BNO055_left_leg']["accel_z"],
                        quat_w=data['BNO055_left_leg']["quat_w"],
                        quat_x=data['BNO055_left_leg']["quat_x"],
                        quat_y=data['BNO055_left_leg']['quat_y'],
                        quat_z=data['BNO055_left_leg']["quat_z"]
                    )
                    left_leg_df = LeftLegSensor(self.db, self.active_session_id).integration()
                    
                    timestamp = left_leg_df.iloc[-1]['timestamp']
                    # if is_naive(timestamp):
                    #     timestamp = make_aware(timestamp)
                        
                    LeftLegTransformed.objects.create(
                        session_id=session,
                        timestamp=timestamp,
                        accel_x=left_leg_df.iloc[-1]['accel_x'],
                        accel_y=left_leg_df.iloc[-1]['accel_y'],
                        accel_z=left_leg_df.iloc[-1]['accel_z'],
                        vel_x=left_leg_df.iloc[-1]['vel_x'],
                        vel_y=left_leg_df.iloc[-1]['vel_y'],
                        vel_z=left_leg_df.iloc[-1]['vel_z'],
                        pos_x=left_leg_df.iloc[-1]['pos_x'],
                        pos_y=left_leg_df.iloc[-1]['pos_y'],
                        pos_z=left_leg_df.iloc[-1]['pos_z']
                    )

                stats = RealTimeStatistics(self.db, self.active_session_id)
                chest_distance = stats.get_BNO_distance('BNO055_chest')
                foot_quality = FootingQuality(self.db, self.active_session_id)
                fatigue = FatigueCalculator(self.db, session_id=self.active_session_id)
                training = PostTrainingAnalysis(self.db)

                print('BPM', stats.BPM())
                SessionStats.objects.create(
                    session_id=session,
                    time=time_now,
                    distance=chest_distance,
                    pace=stats.get_BNO_pace('BNO055_chest'),
                    g=stats.get_BNO_g('BNO055_head'),
                    BPM=stats.BPM(),
                    footing_quality=foot_quality.footing_quality_score(),
                    fatigue_level=fatigue.calculate_fatigue(),
                    training_intensity=training.analyze(session_id=self.active_session_id)['training_intensity'],
                    concussion_risk=training.analyze(session_id=self.active_session_id)['concussion_risk']
                )
                
                ConcussionStats.objects.create(
                    session_id=session,
                    time=time_now,
                    footing_quality=foot_quality.footing_quality_score(),
                    number_of_shocks=training.analyze(session_id=self.active_session_id)['number_of_shocks'],
                    max_g=stats.max_g(),
                    BMP=stats.BPM(),
                    SpO2=stats.SpO2(),
                    temperature=stats.temperature()
                )
                
                async_to_sync(self.send_data_via_websocket)()  # Exécuter send_data_via_websocket dans un contexte synchrone
                print("Data inserted")
        else :
            print("No active session")
       

    
    def create_new_session(self, session_name):
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_session_id = self.get_last_session_id() + 1
        self.db.insert_session(new_session_id, session_name, start_time, None, 0, 0, 0, 0, 0) 
        self.active_session_id = new_session_id
    
                
    def close_session(self):
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_id = self.get_last_session_id()
        self.cursor.execute('''
            UPDATE training_sessions
            SET end_time = ?
            WHERE session_id = ?
            ''', (end_time, session_id))
        self.connection.commit()
        self.active_session_id = None



