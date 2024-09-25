# Fichier pour gérer l'arrivée de data depuis le broker


# Dans ce finchier, il faut gérer l'aarivée de data;
# Donc, créer un nouvel session_id, ajouter les données dans la table des mesures avec le temps


from Database import Database
from datetime import datetime
import sqlite3

class DataHandler:
    def __init__(self, db):
        self.db = db
        self.connection = self.db.connection
        self.cursor = self.db.cursor()

    def get_last_session_id(self):
        self.cursor.execute('''
            SELECT MAX(session_id) FROM sessions
         ''')
        last_session_id = self.cursor.fetchone()[0]
        if last_session_id is None :
            return 0
        return last_session_id
        
    def process_data(self, data):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.insert_measurement(self.get_last_session_id , time, data['accel_x'], data['accel_y'], data['accel_z'], data['eul_x'], data['eul_y'], data['eul_z'])

        
    def create_new_session(self, session_name):
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.insert_session(self.get_last_session_id + 1, session_name, start_time, None, 0, 0, 0, 0, 0) 
            
            
    def close_session(self, session_id):
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            UPDATE sessions
            SET end_time = ?
            WHERE session_id = ?
            ''', (end_time, session_id))
        self.connection.commit()
            
# on insère les mesures à chaque fois, mais il faut faire la distinction de si c'est une nouvelle session ou pas. 
# donc, à chaque début de mesure, on ouvre session, et on la ferme en ajoutant un end_time. On initialise pour l'instant tout à None 