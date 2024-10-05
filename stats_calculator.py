# Contient des fonctions pour calculer les statistiques basées sur les données recueillies.

from Database import Database
from data_handler import DataHandler
import time
import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R  # Pour convertir les quaternions en matrices de rotation


class Statistics :
    def __init__(self, db) :
        self.db = db
        self.measurements = db.to_dataframe_measurements()
        self.sessions = db.to_dataframe_sessions()
        
        
        
class RealTimeStatistics:
    def __init__(self, db):
        self.db = db
        
        self.tables = ['sessions', 'BNO055_head', 'BNO055_chest', 'BNO055_right_leg', 'BNO055_left_leg', 'MAX30102', 'BMP280']
        for table in self.tables:
            df = self.to_dataframe(table) 
            setattr(self, table, df)       # Create an attribut with the table name

        
        self.active_session_id = DataHandler(db).active_session_id
        self.acceleration = [np.zeros((3,1))]                         # Stores the global acceleration vector
        self.g_measurements = [0]                    # 0 to avoid cases where a function tries to use an element that doesn't exist
        self.velocities = [np.zeros((3,1))]                           # Contains the velocities we mesure, without any modification, mainly to compute the distance
        self.velocities_norm = [0]
        self.distance = 0

    
    def start_timer(self):
        start_time = self.sessions.loc[self.sessions['session_id'] == self.active_session_id, 'start_time'].values[0]

        try : 
            while self.active_session_id is not None :
                elapsed_time = time.time() - start_time
                print(f'Time elaspsed : {elapsed_time:.2f} secondes', end='\r')
                time.sleep(0.1)
        except KeyboardInterrupt :
            print('\nTimer stopped.')
    
    ## Here, we are computing general stats for distance, speed and acceleration
    ## We are using the BNO055 on the chest for the stability of measures
    
    def check_session(self):
        if self.active_session_id is not None :
            return np.sum(self.BNO055_chest["id_session"])        ## The number of elements in the last session
        else :
            print("No session is active.")
            return 0
        
    def dt(self):
        if self.check_session() < 3:
            return 0.5  
        last_timestamp = self.BNO055_chest.iloc[-1]['time']
        previous_timestamp = self.BNO055_chest.iloc[-2]['time']
        dt = (last_timestamp - previous_timestamp).total_seconds()  
        return dt if dt > 0 else 0.5  

    
    def compute_acceleration(self, max_size = 100) :
        
        if self.check_session() > 0:
            accel_x = self.BNO055_chest.iloc[-1]["accel_x"]
            accel_y = self.BNO055_chest.iloc[-1]["accel_y"]
            accel_z = self.BNO055_chest.iloc[-1]["accel_z"]
            
            rotation_matrix = R.from_quat(self.BNO055_chest.iloc[-1]['quat_w'], 
                                            self.BNO055_chest.iloc[-1]['quat_x'], 
                                            self.BNO055_chest.iloc[-1]['quat_y'], 
                                            self.BNO055_chest.iloc[-1]['quat_z']).as_matrix()
            
            local_acceleration = np.array([accel_x, accel_y, accel_z])
            global_acceleration = np.dot(rotation_matrix.T, local_acceleration)
            
            self.acceleration.append(global_acceleration)
            self.g_measurements.append(np.linalg.norm(global_acceleration)/9.81)  # Acceleration norm
            
            if len(self.acceleration) > max_size :
                self.acceleration.pop(0)



    # We have to take a sufficient amount of data 
    def pace(self, window_size=10, max_size = 100):
        
        velocity = self.velocities[-1] + self.acceleration[-1] * self.dt()
        self.velocities.append(velocity)
        velocity_norm = np.linalg.norm(velocity)
        self.velocities_norm.append(velocity_norm)
        
        if len(self.velocities_norm) < window_size:
            pace = velocity_norm
        else :                 
            pace = np.mean(self.velocities_norm[-window_size:])       # Mean on the ten last velocity values
                    
        if len(self.velocities) > max_size :
            self.velocities.pop(0)
            
        return pace
    

    # it is not correlated with the pace function because we want the exact distance and the function pace is a mean
    def compute_distance(self):
        if len(self.velocities_norm) > 1:
            dt = self.dt()
            if dt > 0:
                self.distance += self.velocities_norm[-1] * dt
        return self.distance
            
       
    
        

class RealTimePlotter:
    def __init__(self) -> None:
        pass
    
    
    
db = Database('Database.db')
data_measure = db.to_dataframe_measurements()


# stats = Statistics(db)

# ActualStats = RealTimeStatistics(db)

print('measurements :')
print(data_measure)

# print('sessions :')
# print(stats.sessions)