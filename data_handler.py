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
                self.db.insert_measurement(self.active_session_id, time, data['accel_x'], data['accel_y'], data['accel_z'], data['quat_w'], data['quat_x'], data['quat_y'], data['quat_z'])
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
