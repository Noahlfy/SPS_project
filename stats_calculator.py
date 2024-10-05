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
        self.measurements = db.to_dataframe_measurements()
        self.sessions = db.to_dataframe_sessions()
        self.active_session_id = DataHandler(db).active_session_id
        self.acceleration = [0]                         # To avoid cases where a function tries to use an element that doesn't exist
        self.pace = [0]                                 # To avoid cases where a function tries to use an element that doesn't exist
        self.velocities = [0]                           # Contains the velocities we mesure, without any modification, mainly to compute the distance
        self.distance = 0

    
    
    def start_timer(self):
        start_time =  self.sessions.loc[self.sessions['session_id'] == self.active_session_id, 'start_time'].values[0], 
        try : 
            while self.active_session_id is not None :
                elapsed_time = time.time() - start_time
                print(f'Time elaspsed : {elapsed_time:.2f} secondes', end='\r')
                time.sleep(0.1)
        except KeyboardInterrupt :
            print('\nTimer stopped.')
    
    
    def compute_dt(self):
        if len(self.measurements) < 2:
            return 0.5  
        last_timestamp = self.measurements.loc[self.measurements["BNO055_head"] = "accel_x", :].iloc[-1]['time']
        previous_timestamp = self.measurements.iloc[-2]['time']
        dt = (last_timestamp - previous_timestamp).total_seconds()  
        return dt if dt > 0 else 0.5  

    
    def compute_acceleration(self, max_size = 100) :
        accel_x = self.measurements.iloc[-1]["accel_x"]
        accel_y = self.measurements.iloc[-1]["accel_y"]
        accel_z = self.measurements.iloc[-1]["accel_z"]
        
        rotation_matrix = R.from_quat(self.measurements.iloc[-1]['quat_w'], 
                                          self.measurements.iloc[-1]['quat_x'], 
                                          self.measurements.iloc[-1]['quat_y'], 
                                          self.measurements.iloc[-1]['quat_z']).as_matrix()
        local_acceleration = np.array([accel_x, accel_y, accel_z])
        global_acceleration = np.dot(rotation_matrix.T, local_acceleration)
        self.acceleration.append(np.linalg.norm(global_acceleration))  # Acceleration norm
        
        if len(self.acceleration) > max_size :
            self.acceleration.pop(0)


    # We have to take a sufficient amount of data 
    def compute_pace(self, window_size=10, max_size = 100):
        dt = self.compute_dt()
        if len(self.acceleration) < window_size:
            self.pace.append(self.pace[-1] + self.acceleration[-1] * dt)
        else : 
            velocities = [self.pace[-1]]
            for i in range(1, window_size) :
                velocities.append(velocities[-1] + self.acceleration[i-window_size]*dt)

            velocities = pd.Series(velocities)
            self.pace.append(velocities.mean())
            
        if len(self.pace) > max_size :
            self.pace.pop(0)
    
    def compute_velocities(self, max_size = 100) :
        dt = self.compute_dt()
        self.velocities.append(self.velocities[-1] + self.acceleration[-1] * dt)
        
        if len(self.velocities) > max_size :
            self.velocities.pop(0)
        
    # it is not correlated with the pace function (or self.pace) because we want the exact distance and the function pace is a mean
    def compute_distance(self):
        dt = self.compute_dt()
        if len(self.velocities) > 1 :
            self.distance += self.velocities[-1] * dt
       
    
        

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