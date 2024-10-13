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


db = Database('database.db')
data_handler = DataHandler(db)
mqtt_client = MQTTClient("localhost", "esp32/output", data_handler)

db.create_tables()

@app.route('/start_session', methods=['POST'])
def start_session():
    session_name = request.form.get('session_name', 'Default Session')
    if session_name == "" :
        session_name = session_name = "Session_" + str(data_handler.get_last_session_id())
    data_handler.create_new_session(session_name)
    
    # Démarrer le client MQTT dans un thread séparé
    threading.Thread(target=mqtt_client.start).start()
    print(f"Data collection started for session: {session_name}")
    return "Data collection started!"

@app.route('/pause_session', methods=['POST'])
def pause_session():
    # Logique pour mettre la session en pause (si nécessaire)
    data_handler.pause_session()
    return "Session paused!"

@app.route('/stop_session', methods=['POST'])
def stop_session():
    mqtt_client.stop()
    data_handler.close_session()
    return "Data collection stopped and session closed!"


# Route pour la page Dashboard
@app.route('/')
@app.route('/index.html')
def dashboard():
    return render_template('index.html')

# Route pour la page Database
@app.route('/database.html')
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

