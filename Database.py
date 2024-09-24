# Classe dédiée à la gestion de la base de données SQLite. Elle inclura des méthodes pour créer des tables, insérer des données, et interroger les données stockées.

import sqlite3

class Database:
    def __init__(self, db_name = 'Database.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()
        
        
    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER,
            start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            end_time DATE_TIME,
            acceleration_max REAL,
            speed_max REAL,
            total_distance REAL,
            commotion_risk INTEGER,
            fatigue_level REAL
        )                           
        ''' )
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER AUTOINCREMENT,
            session_id INTEGER
            time DATETIME DEFAULT CURRENT_TIMESTAMP,
            accel_x REAL,
            accel_y REAL,
            accel_z REAL,
            eul_x REAL,
            eul_y REAL,
            eul_z REAL,
                CONSTRAINT FK_measurements_session_id FOREIGN_KEY (session_id) REFERENCES sessions session_id,
                CONSTRAINT PK_measurements            PRIMARY_KEY (ID);
        )                        
        ''')
        
        self.connection.commit()
        
    def insert_session(self, sessions_id, start_time, end_time, acceleration_max, speed_max, total_distance, commotion_risk, fatigue_level):
        self.cursor.execute('''
            INSERT INTO sessions (sessions_id, start_time, end_time, acceleration_max, speed_max, total_distance, commotion_risk, fatigue_level)
        ''', (sessions_id, start_time, end_time, acceleration_max, speed_max, total_distance, commotion_risk, fatigue_level))
        self.connection.commit()
        
        
    def insert_measurement(self, id, session_id, time, accel_x, accel_y, accel_z, eul_x, eul_y, eul_z): 
        self.cursor.execute('''
            INSERT INTO sessions (id, session_id, time, accel_x, accel_y, accel_z, eul_x, eul_y, eul_z)
        ''', (id, session_id, time, accel_x, accel_y, accel_z, eul_x, eul_y, eul_z))
        self.connection.commit()