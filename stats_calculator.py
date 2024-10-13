# Contient des fonctions pour calculer les statistiques basées sur les données recueillies.

from Database import Database
from data_handler import DataHandler
import time
import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R  # Pour convertir les quaternions en matrices de rotation

class BNO05Sensor:
    def __init__(self, name, db, initial_position, session_id):
        self.db = db
        self.name = name
        self.session_id = session_id

        self.g_measurements = [0]                            # 0 to avoid cases where a function tries to use an element that doesn't exist
        self.velocities_norm = [0]                           # 0 to avoid cases where a function tries to use an element that doesn't exist 
        self.distance = 0
        
        #Recreate a dataframe for our js interface (easily exported in json)
        self.df = pd.DataFrame({
            'timestamp': [self.data.iloc[-1]['time']],      
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
        
    def update_data(self):
        # Dynamically fetch the latest data for the active session from the database
        query = f"SELECT * FROM {self.name} WHERE session_id = {self.session_id} ORDER BY time DESC LIMIT 1"
        new_data = pd.read_sql(query, self.db.conn)  # Re-fetch data from the DB
        
         # Check if new data is available, skip if empty
        if new_data.empty:
            print("No new data received. Skipping calculation step.")
            return
    
        # Proceed with integration only if new data is available
        self.data = new_data
       
    def check_session(self):
        """Check if there is an active session and return the number of elements in the last session."""
        if self.active_session_id is not None :
            return np.sum(self.data["id_session"])        ## The number of elements in the last session
        else :
            print("No session is active.")
            return 0
        
    def dt(self):
        if self.check_session() < 2:
            return 0.5
        last_timestamp = self.data.iloc[-1]['time']
        previous_timestamp = self.data.iloc[-2]['time']
        dt = (last_timestamp - previous_timestamp).total_seconds()
        return dt if dt > 0 else 0.5 
    
    def integration(self, max_size=100):
        self.update_data()
        if self.check_session() > 0:
            
            ## Compute aceeleration
            accel_x = self.data.iloc[-1]["accel_x"]
            accel_y = self.data.iloc[-1]["accel_y"]
            accel_z = self.data.iloc[-1]["accel_z"]
            
            rotation_matrix = R.from_quat(self.data.iloc[-1]['quat_w'], 
                                            self.data.iloc[-1]['quat_x'], 
                                            self.data.iloc[-1]['quat_y'], 
                                            self.data.iloc[-1]['quat_z']).as_matrix()
            
            local_acceleration = np.array([accel_x, accel_y, accel_z])
            global_acceleration = np.dot(rotation_matrix.T, local_acceleration)
            
            self.g_measurements.append(np.linalg.norm(global_acceleration)/9.81)  # Acceleration norm

                                   
            ## Compute velocity         
            velocity = self.df.iloc[-1][['vel_x', 'vel_y', 'vel_z']] + global_acceleration * self.dt()
            velocity_norm = np.linalg.norm(velocity)
            self.velocities_norm.append(velocity_norm)
                        
            ## Compute position
            position = self.df.iloc[-1][['pos_x', 'pos_y', 'pos_z']] + velocity * self.dt()
            
            self.df = self.df.append({
                'timestamp': self.data.iloc[-1]['time'],
                'accel_x': global_acceleration[0],
                'accel_y': global_acceleration[1],
                'accel_z': global_acceleration[2],
                'vel_x': velocity[0],
                'vel_y': velocity[1],
                'vel_z': velocity[2],
                'pos_x': position[0],
                'pos_y': position[1],
                'pos_z': position[2]
            }, ignore_index=True)            

            return self.df
    def compute_g(self) :
            self.g_measurements[-1]  # Acceleration norm
            
    # We have to take a sufficient amount of data 
    def pace(self, window_size=10):
        
        if len(self.velocities_norm) < window_size:
            pace = self.velocities_norm[-1]
        else :                 
            pace = np.mean(self.velocities_norm[-window_size:])       # Mean on the ten last velocity values
        return pace
    

    def compute_distance(self):
        if len(self.df) > 1:
            pos_prev = self.df.iloc[-2][['pos_x', 'pos_y', 'pos_z']].to_numpy()
            pos_curr = self.df.iloc[-1][['pos_x', 'pos_y', 'pos_z']].to_numpy()
            delta_position = np.linalg.norm(pos_curr - pos_prev)
            self.distance += delta_position
        return self.distance

        
    
## Description of the position of the sensor (all same z and same orientation):
#   - x bottom -> top
#   - y left -> right
#   - z back -> front
## For the percentages, we should find documentation because thesse are approximations

class HeadSensor(BNO05Sensor):
    def __init__(self, db, session_id, player_height=1.80):
        initial_position = (player_height * 0.97, 0, 0)
        super().__init__('BNO055_head', db, session_id, initial_position)
        
class ChestSensor(BNO05Sensor):
    def __init__(self, db, session_id, player_height=1.80):
        initial_position = (player_height * 0.60, 0, 0)
        super().__init__('BNO055_chest', db, session_id, initial_position)
        
class RightlegSensor(BNO05Sensor):
    def __init__(self, db, session_id, player_height = 1.80, player_width = 0.4):
        initial_position = (player_height * 0.33, +player_width * 0.20, 0)
        super().__init__('BNO055_right_leg', db, session_id, initial_position)
        
class LeftLegSensor(BNO05Sensor):
    def __init__(self, db, session_id, player_height = 1.80, player_width = 0.4):
        initial_position = (player_height * 0.33, -player_width * 0.20, 0)
        super().__init__('BNO055_left_leg', db, session_id, initial_position)
        

class RealTimeStatistics:
    def __init__(self, db):
        self.db = db
        
        self.active_session_id = DataHandler(db).active_session_id
        
        self.head_sensor = HeadSensor(db, session_id=self.active_session_id)
        self.chest_sensor = ChestSensor(db, session_id=self.active_session_id)
        self.right_leg_sensor = RightlegSensor(db, session_id=self.active_session_id)
        self.left_leg_sensor = LeftLegSensor(db, session_id=self.active_session_id)
        self.BMP280 = db.to_dataframe("BMP280")
        self.MAX30102 = db.to_dataframe("MAX30102")       
        
    ## END OF INITIALIZING 

    def start_timer(self):
        start_time = self.sessions.loc[self.sessions['session_id'] == self.active_session_id, 'start_time'].values[0]
        try : 
            while self.active_session_id is not None :
                elapsed_time = time.time() - start_time
                print(f'Time elaspsed : {elapsed_time:.2f} secondes', end='\r')
                time.sleep(0.1)
        except KeyboardInterrupt :
            print('\nTimer stopped.')
    
    
    def get_BNO_data(self, sensor_name):
        if sensor_name == 'BNO055_head':
            return self.head_sensor.integration()  # Call integration for real-time update
        if sensor_name == 'BNO055_chest':
            return self.chest_sensor.integration()
        if sensor_name == 'BNO055_right_leg':
            return self.right_leg_sensor.integration()
        if sensor_name == 'BNO055_left_leg':
            return self.left_leg_sensor.integration()
    
    def get_BNO_g(self, sensor_name):
        if sensor_name == 'BNO055_head':
            return self.head_sensor.compute_g()  # Call compute_g for real-time update
        if sensor_name == 'BNO055_chest':
            return self.chest_sensor.compute_g()
        if sensor_name == 'BNO055_right_leg':
            return self.right_leg_sensor.compute_g()
        if sensor_name == 'BNO055_left_leg':
            return self.left_leg_sensor.compute_g()
 
    def get_BNO_pace(self, sensor_name):
        if sensor_name == 'BNO055_head':
            return self.head_sensor.pace()  # Call pace for real-time update
        if sensor_name == 'BNO055_chest':
            return self.chest_sensor.pace()
        if sensor_name == 'BNO055_right_leg':
            return self.right_leg_sensor.pace()
        if sensor_name == 'BNO055_left_leg':
            return self.left_leg_sensor.pace()
 
    def get_BNO_distance(self, sensor_name):
        if sensor_name == 'BNO055_head':
            return self.head_sensor.compute_distance()  # Call compute_distance for real-time update
        if sensor_name == 'BNO055_chest':
            return self.chest_sensor.compute_distance()
        if sensor_name == 'BNO055_right_leg':
            return self.right_leg_sensor.compute_distance()
        if sensor_name == 'BNO055_left_leg':
            return self.left_leg_sensor.compute_distance()
    
    def relative_position(self, BNO_1, BNO_2):
        df1 = self.get_BNO_data(BNO_1)
        df2 = self.get_BNO_data(BNO_2)
        
        pos1 = df1[['pos_x', 'pos_y', 'pos_z']].iloc[-1].to_numpy()
        pos2 = df2[['pos_x', 'pos_y', 'pos_z']].iloc[-1].to_numpy()
        
        relative_pos = pos2 - pos1
        
        return relative_pos

    def Temperature(self):
        return self.BMP280.iloc[-1]["temperature"]
        
    def Pressure(self):
        return self.BMP280.iloc[-1]["pressure"]
            
    def Altitude(self):
        return self.BMP280.iloc[-1]["altitude"]
    
    def BPM(self):
        return self.MAX30102[-1]["BPM"]
    
    def SpO2(self):
        return self.MAX30102[-1]["SpO2"]
    
## CREATE A CLASS CHOC, FOR, WHEN A CHOC HAPPENS, MULTIPLE DATA APPEARS
## Mettre en place le CUMULATIVE HEAD IMPACT
## Ne pas oublier BPM et SpO2
## Notification visuelle et sonore quand le suil est dépassé


class Statistics :
    def __init__(self, db) :
        self.db = db
        self.sessions = db.to_dataframe_sessions()
        
class RealTimePlotter:
    def __init__(self) -> None:
        pass
    
    
    
