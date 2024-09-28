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
        
    def start_timer(self):
        start_time =  self.sessions.loc[self.sessions['session_id'] == self.active_session_id, 'start_time'].values[0], 
        try : 
            while self.active_session_id is not None :
                elapsed_time = time.time() - start_time
                print(f'Time elaspsed : {elapsed_time:.2f} secondes', end='\r')
                time.sleep(0.1)
        except KeyboardInterrupt :
            print('\nTimer stopped.')
    
    # We have to take a sufficient amount of data 
    def pace(self, window_size=10):
        
        session_measurements = self.measurements[self.measurements['session_id'] == self.active_session_id]
        
        if len(session_measurements) < window_size:
            return 0
        
        recent_data = session_measurements.tail(window_size)
        
        dt = 0.5
        velocities = [0]
        accelerations = []
        for i in range(1, len(recent_data)) :
            accel_x = recent_data.iloc[i]['accel_x']
            accel_y = recent_data.iloc[i]['accel_y']
            accel_z = recent_data.iloc[i]['accel_z']
            rotation_matrix = R.from_quat(recent_data.iloc[i]['quat_w'], 
                                          recent_data.iloc[i]['quat_x'], 
                                          recent_data.iloc[i]['quat_y'], 
                                          recent_data.iloc[i]['quat_z']).as_matrix()
            
            local_acceleration = np.array(accel_x, accel_y, accel_z)
            global_acceleration = np.dot(rotation_matrix.T, local_acceleration)
            accelerations.append(np.linalg.norm(global_acceleration))  # Acceleration norm
            
            if i != 1:
                velocities.append(velocities[i-1] + accelerations[i]**dt)

        velocities = pd.Series(velocities)
        velocity = velocities.mean()
        return velocity
       
    

    def distance(self):
        
        session_measurements = self.sessions[self.sessions['session_id'] == self.active_session_id]
        
        
        
        return 0
    
        

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