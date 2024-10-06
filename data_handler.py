# Fichier pour gérer l'arrivée de data depuis le broker


import threading
from Database import Database
from datetime import datetime
import sqlite3

class DataHandler:
    def __init__(self, db):
        self.db = db
        self.connection = self.db.connection
        self.cursor = self.db.connection.cursor()
        self.active_session_id = None
        self.lock = threading.Lock()  # Verrou pour accès concurrent à la base


    def get_last_session_id(self):
        if self.db.check_table_exists("sessions") == True : 
            self.cursor.execute('''
                SELECT MAX(session_id) FROM sessions
            ''')
            last_session_id = self.cursor.fetchone()[0]
            if last_session_id is None :
                return 0
            return last_session_id
        return 0
        
    def process_data(self, data):
        if self.active_session_id is not None : 
            print("Processing data : ", data)
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            
            with self.lock:  # Utilisation du verrou lors de l'accès à la base
                print(f"Inserting measures for session {self.get_last_session_id()}")
                
                if 'MAX30102' in data :
                    self.db.insert_MAX30102(self.active_session_id, time, data['MAX30102']["SpO2"], data['MAX30102']['BPM'])
                if 'BMP280' in data :
                    self.db.insert_BMP280(self.active_session_id, time, data['BMP280']["temperature"], data['BMP280']['pressure'], data['BMP280']['altitude'])                   
                if 'BNO055_head' in data :
                    self.db.insert_BNO055('BNO055_head', self.active_session_id, time, "BNO055_head", data['BNO055_head']["accel_x"], data['BNO055_head']['accel_y'], data['BNO055_head']["accel_z"], 
                                            data['BNO055_head']["quat_w"], data['BNO055_head']["quat_x"], data['BNO055_head']['quat_y'], data['BNO055_head']["quat_z"])
                if 'BNO055_chest' in data :
                    self.db.insert_BNO055('BNO055_chest', self.active_session_id, time, "BNO055_chest", data['BNO055_chest']["accel_x"], data['BNO055_chest']['accel_y'], data['BNO055_chest']["accel_z"], 
                                            data['BNO055_chest']["quat_w"], data['BNO055_chest']["quat_x"], data['BNO055_chest']['quat_y'], data['BNO055_chest']["quat_z"])
                if 'BNO055_right_leg' in data :
                    self.db.insert_BNO055('BNO055_right_leg', self.active_session_id, time, "BNO055_right_leg", data['BNO055_right_leg']["accel_x"], data['BNO055_right_leg']['accel_y'], 
                                          data['BNO055_right_leg']["accel_z"], data['BNO055_right_leg']["quat_w"], data['BNO055_right_leg']["quat_x"], data['BNO055_right_leg']['quat_y'], 
                                          data['BNO055_right_leg']["quat_z"])
                if 'BNO055_left_leg' in data :
                    self.db.insert_BNO055('BNO055_left_leg', self.active_session_id, time, "BNO055_left_leg", data['BNO055_left_leg']["accel_x"], data['BNO055_left_leg']['accel_y'], 
                                          data['BNO055_left_leg']["accel_z"], data['BNO055_left_leg']["quat_w"], data['BNO055_left_leg']["quat_x"], data['BNO055_left_leg']['quat_y'], 
                                          data['BNO055_left_leg']["quat_z"])
        else :
            print("No session started. Measures not registered.")        

    
    def create_new_session(self, session_name):
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_session_id = self.get_last_session_id() + 1
        self.db.insert_session(new_session_id, session_name, start_time, None, 0, 0, 0, 0, 0) 
        self.active_session_id = new_session_id
            
    def close_session(self):
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_id = self.get_last_session_id()
        self.cursor.execute('''
            UPDATE sessions
            SET end_time = ?
            WHERE session_id = ?
            ''', (end_time, session_id))
        self.connection.commit()
        self.active_session_id = None

    