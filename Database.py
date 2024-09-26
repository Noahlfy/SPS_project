import sqlite3

class Database:
    def __init__(self, db_name='Database.db'):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()
        
    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY,  
            session_name VARCHAR(50),
            start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            end_time DATETIME,
            acceleration_max REAL,
            speed_max REAL,
            total_distance REAL,
            commotion_risk INTEGER,
            fatigue_level REAL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            session_id INTEGER,
            time DATETIME DEFAULT CURRENT_TIMESTAMP,
            accel_x REAL,
            accel_y REAL,
            accel_z REAL,
            eul_x REAL,
            eul_y REAL,
            eul_z REAL,
            CONSTRAINT FK_measurements_session_id FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
        ''')
        
        self.connection.commit()
        
    def delete_tables(self):
        self.cursor.execute('DROP TABLE IF EXISTS sessions')
        self.cursor.execute('DROP TABLE IF EXISTS measurements')
        
    def check_table_exists(self, table_name):
        self.cursor.execute('''
            SELECT name FROM sqlite_master WHERE type='table' AND name=?
        ''', (table_name,))
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False

    def insert_session(self, session_id, session_name, start_time, end_time, acceleration_max, speed_max, total_distance, commotion_risk, fatigue_level):
        self.cursor.execute('''
            INSERT INTO sessions (session_id, session_name, start_time, end_time, acceleration_max, speed_max, total_distance, commotion_risk, fatigue_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, session_name, start_time, end_time, acceleration_max, speed_max, total_distance, commotion_risk, fatigue_level))
        self.connection.commit()

        
    def insert_measurement(self, session_id, time, accel_x, accel_y, accel_z, eul_x, eul_y, eul_z): 
        self.cursor.execute('''
            INSERT INTO measurements (session_id, time, accel_x, accel_y, accel_z, eul_x, eul_y, eul_z)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, time, accel_x, accel_y, accel_z, eul_x, eul_y, eul_z))
        self.connection.commit()
        
    def delete_session(self, session_id):
        self.cursor.execute('''
        DELETE FROM sessions WHERE session_id = ?
        ''', (session_id,))
        self.connection.commit() 
        
    def delete_measurement(self, measurement_id):
        self.cursor.execute('''
        DELETE FROM measurements WHERE id = ?
        ''', (measurement_id,))
        self.connection.commit()   
    
    def fetch_all_measurements(self):
        self.cursor.execute('SELECT * FROM measurements')
        return self.cursor.fetchall()

    def fetch_all_sessions(self):
        self.cursor.execute('SELECT * FROM sessions')
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()



    