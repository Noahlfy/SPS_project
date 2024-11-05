import sqlite3
import pandas as pd

class Database:
    def __init__(self, db_name='Database.db'):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

    # CREATE
    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS session (
            session_id INTEGER PRIMARY KEY,  
            session_name VARCHAR(50),
            start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            end_time DATETIME,
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS BNO055_head (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            session_id INTEGER,
            time DATETIME DEFAULT CURRENT_TIMESTAMP,
            accel_x REAL,
            accel_y REAL,
            accel_z REAl,
            quat_w REAL,                 
            quat_x REAL,                 
            quat_y REAL,                 
            quat_z REAL,                 
            CONSTRAINT FK_BNO055_head_session_id FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS BNO055_chest (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            session_id INTEGER,
            time DATETIME DEFAULT CURRENT_TIMESTAMP,
            accel_x REAL,
            accel_y REAL,
            accel_z REAl,
            quat_w REAL,                 
            quat_x REAL,                 
            quat_y REAL,                 
            quat_z REAL,                 
            CONSTRAINT FK_BNO055_chest_session_id FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS BNO055_left_leg (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            session_id INTEGER,
            time DATETIME DEFAULT CURRENT_TIMESTAMP,
            accel_x REAL,
            accel_y REAL,
            accel_z REAL,
            quat_w REAL,                 
            quat_x REAL,                 
            quat_y REAL,                 
            quat_z REAL,                 
            CONSTRAINT FK_BNO055_left_leg_session_id FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS BNO055_right_leg (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            session_id INTEGER,
            time DATETIME DEFAULT CURRENT_TIMESTAMP,
            accel_x REAL,
            accel_y REAL,
            accel_z REAl,
            quat_w REAL,                 
            quat_x REAL,                 
            quat_y REAL,                 
            quat_z REAL,                 
            CONSTRAINT FK_BNO055_right_leg_session_id FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS MAX30102 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            time DATETIME DEFAULT CURRENT_TIMESTAMP,
            SpO2 REAL,
            BPM INTEGER,
            CONSTRAINT FK_MAX30102_session_id FOREIGN KEY (session_id) REFERENCES sessions(session_id)
          )                  
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS BMP280 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            time DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL,
            pressure REAL,
            CONSTRAINT FK_BMP280_session_id FOREIGN KEY (session_id) REFERENCES sessions(session_id)
          )                  
        ''')

        self.connection.commit()
    
    
    ## DELETE ALL TABLES
    def delete_tables(self):
        tables = ['training_sessions', 'BNO055_head', 'BNO055_chest', 'BNO055_right_leg', 'BNO055_left_leg', 'MAX30102', 'BMP280']
        
        for table in tables :
            self.cursor.execute(f'DROP TABLE IF EXISTS {table}')
        self.connection.commit()
        
    ## DELETE SESSIONS
    def delete_session(self, session_id):
        tables = ['training_sessions', 'BNO055_head', 'BNO055_chest', 'BNO055_right_leg', 'BNO055_left_leg', 'MAX30102', 'BMP280']
        
        for table in tables:
            self.cursor.execute(f"DELETE FROM {table} WHERE session_id = ?", (session_id,))
        self.connection.commit()
    
    
    ## WE COULD THINK OF A FUNCTION THAT DELETES A SINGLE MEASUREMENT IN FUNCTION OF THE TIME BUT NOT VERY USEFUL SINCE WE NEED TO KNOW THE EXACT TIME
    # def delete_measurement(self, measurement_id):
    #     self.cursor.execute('''
    #     DELETE FROM measurements WHERE id = ?
    #     ''', (measurement_id,))
    #     self.connection.commit()   

    ## CHECK
    def check_table_exists(self, table_name):
        self.cursor.execute('''
            SELECT name FROM sqlite_master WHERE type='table' AND name=?
        ''', (table_name,))
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False
             
    ## INSERTS
    def insert_session(self, session_id, session_name, start_time, end_time):
        self.cursor.execute('''
            INSERT INTO training_sessions (session_id, session_name, start_time, end_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, session_name, start_time, end_time))
        self.connection.commit()
        
    def insert_BNO055(self, sensor_name, session_id_id, time, accel_x, accel_y, accel_z, quat_w, quat_x, quat_y, quat_z): 
        query = f'''INSERT INTO {sensor_name} (session_id_id, time, accel_x, accel_y, accel_z, quat_w, quat_x, quat_y, quat_z)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        self.cursor.execute(query, (session_id_id, time, accel_x, accel_y, accel_z, quat_w, quat_x, quat_y, quat_z))
        self.connection.commit()

        
    def insert_MAX30102(self, session_id_id, time, SpO2, BPM) :
        self.cursor.execute('''
        INSERT INTO MAX30102 (session_id_id, time, SpO2, BPM)
        VALUES (?, ?, ?, ?)
        ''', (session_id_id, time, SpO2, BPM))
        self.connection.commit()
    
    def insert_BMP280(self, session_id_id, time, temperature, pressure) :
        self.cursor.execute('''
        INSERT INTO BMP280 (session_id_id, time, temperature, pressure)
        VALUES (?, ?, ?, ?)
        ''', (session_id_id, time, temperature, pressure))
        self.connection.commit()
    
    def insert_BNO055_transformed (self, sensor_name, session_id_id, timestamp, accel_x, accel_y, accel_z, vel_x, vel_y, vel_z, pos_x, pos_y, pos_z) :
        self.cursor.execute(f'''
        INSERT INTO {sensor_name}_transformed (session_id_id, timestamp, accel_x, accel_y, accel_z, vel_x, vel_y, vel_z, pos_x, pos_y, pos_z)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id_id, timestamp, accel_x, accel_y, accel_z, vel_x, vel_y, vel_z, pos_x, pos_y, pos_z))
    
    def insert_session_stats(self, session_id_id, time, distance, pace, g, heart_rate, footing_quality, fatigue_level, training_intensity, concussion_risk):
        self.cursor.execute('''
        INSERT INTO session_stats (session_id_id, time, distance, pace, g, heart_rate, footing_quality, fatigue_level, training_intensity, concussion_risk)))
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id_id, time, distance, pace, g, heart_rate, footing_quality, fatigue_level, training_intensity, concussion_risk))
        self.connection.commit()
    
    def insert_concussion_stats(self, session_id_id, time, footing_quality, number_of_shocks, max_g, heart_rate, SpO2, temperature) :
        self.cursor.execute('''
        INSERT INTO concussion_stats (session_id_id, time, footing_quality, number_of_shocks, max_g, heart_rate, SpO2, temperature)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (session_id_id, time, footing_quality, number_of_shocks, max_g, heart_rate, SpO2, temperature))
        self.connection.commit()
        
    def insert_dashboard_stats(self, session_id_id, time, training_productivity, concussion_risk, rest_days, concussion_passeport, training_intensity, heart_rate) :
        self.cursor.execute('''
        INSERT INTO dashboard_stats (session_id_id, time, training_productivity, concussion_risk, rest_days, concussion_passeport, training_intensity, heart_rate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id_id, time, training_productivity, concussion_risk, rest_days, concussion_passeport, training_intensity, heart_rate))
        self.connection.commit()
    
    
    ## SHOW TABLES
    
   
    def fetch_all(self, sensor_name):
        self.cursor.execute(f'SELECT * FROM {sensor_name}')
        return self.cursor.fetchall()

    ## TRANSFORM DATA TO DATAFRAME
    def to_dataframe(self, sensor_name):
        query = f"SELECT * from {sensor_name}"
        df = pd.read_sql_query(query, self.connection)
        return df
    
    def to_dataframe_id(self, sensor_name, session_id):
        query = f"SELECT * from {sensor_name} WHERE session_id_id = {session_id}"
        df = pd.read_sql_query(query, self.connection)
        return df

    def close(self):
        self.connection.close()
        
    def drop_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
        tables = self.cursor.fetchall()
        for table_name in tables:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name[0]};")
            print(f"Table {table_name[0]} supprimée.")

        return [table[0] for table in tables]
    
    def delete_records(self, table_name, session_id):
        self.cursor.execute(f"DELETE FROM {table_name} WHERE session_id_id = ?;", (session_id,))
        print(f"Records in table {table_name} with session_id {session_id} have been deleted.")


        
    def show_columns(self, table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = self.cursor.fetchall()
        return [column[1] for column in columns]  # Extraction des noms de colonnes

