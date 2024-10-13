from Database import Database
from mqtt_client import MQTTClient
from data_handler import DataHandler
from stats_calculator import RealTimeStatistics
from flask import Flask
import threading
from flask import Flask, request, jsonify, render_template
import time
import sqlite3

# from stats_calculator import RealTimePlotter


app = Flask(__name__)

db = Database("database.db")
data_handler = DataHandler(db)
mqtt_client = MQTTClient("172.20.10.10", "esp32/output", data_handler)

mqtt_client.start()
db.create_tables()

# Variables globales pour gérer l'état de la session
session_active = False
data_thread = None
session_name = ""

def process_data():
    global session_active
    while session_active:
        # Code pour collecter des données en continu
        print("Collecting data...")
        time.sleep(1)  # Simule un délai entre chaque collecte

@app.route('/api/session', methods=['POST'])
def session_control():
    global session_active, data_thread, session_name

    data = request.json
    action = data.get('action')

    if action == 'start':
        session_name = data.get('sessionName', "")
        print('Code started')
        if session_name == "":
            session_name = "Session_" + str(data_handler.get_last_session_id())
        
        # Démarrer une nouvelle session
        data_handler.create_new_session(session_name)
        session_active = True

        # Démarrer un thread pour la collecte des données
        data_thread = threading.Thread(target=process_data)
        data_thread.start()

        return jsonify({'status': 'session started'}), 200

    elif action == 'pause':
        session_active = False
        data_handler.pause_session()
        return jsonify({'status': 'session paused'}), 200

    elif action == 'exit':
        session_active = False
        data_handler.pause_session()
        return jsonify({'status': 'session stopped'}), 200

    else:
        return jsonify({'error': 'Invalid action'}), 400

if __name__ == '__main__':
    app.run(debug=True)



# Route pour la page Dashboard
@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Route pour la page Database
@app.route('/database')
def database():
    return render_template('database.html')

# Route pour la page Parameters (About)
@app.route('/parameters')
def parameters():
    return render_template('parameters.html')

# API pour récupérer les données en fonction du capteur sélectionné
@app.route('/api/data', methods=['GET'])
def get_data():
    sensor_type = request.args.get('sensor')  # Récupère le capteur sélectionné depuis le front-end
    session_id = request.args.get('session_id', None)  # Optionnel, si on veut filtrer par session

    # Dictionnaire pour mapper le capteur à la bonne table dans la base de données
    sensor_tables = {
        'BNO055_head': 'BNO055_head',
        'BNO055_chest': 'BNO055_chest',
        'BNO055_left_leg': 'BNO055_left_leg',
        'BNO055_right_leg': 'BNO055_right_leg',
        'MAX30102': 'MAX30102',
        'BMP280': 'BMP280'
    }

    # Vérifier si le capteur sélectionné est valide
    if sensor_type not in sensor_tables:
        return jsonify({'error': 'Invalid sensor type'}), 400

    conn = sqlite3.connect('database.db') 
    cursor = conn.cursor()
    query = f"SELECT * FROM {sensor_type}"
    params = []

    # Si un session_id est fourni, ajouter le filtre à la requête
    if session_id:
        query += " WHERE session_id = ?"
        params.append(session_id)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    # Formater les résultats sous forme de liste de dictionnaires
    data = [dict(row) for row in rows]

    # Fermer la connexion
    conn.close()

    # Retourner les données en format JSON
    return jsonify(data)

# Lancer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)

