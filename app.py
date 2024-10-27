from Database import Database
from mqtt_client import MQTTClient
from data_handler import DataHandler
from stats_calculator import RealTimeStatistics
from flask import Flask
import threading
from flask import Flask, request, jsonify, render_template, g
import time
import sqlite3
import json
# from stats_calculator import RealTimePlotter


app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Route pour la page Dashboard
@app.route('/')
@app.route('/index.html')
def dashboard():
    return render_template('index.html')

# Route pour la page Database
@app.route('/database.html')
def database():
    return render_template('database.html')

@app.route('/session.html')
def session():
    return render_template('session.html')

@app.route('/commotion.html')
def commotion():
    return render_template('commotion.html')

# Route pour la page Parameters (About)
@app.route('/parameters.html')
def parameters():
    return render_template('parameters.html')




db = Database('database.db')
data_handler = DataHandler(db)
# stats = RealTimeStatistics(db)
# Créer trois instances séparées
mqtt_client_1 = MQTTClient("localhost", "esp32/output1", data_handler)
mqtt_client_2 = MQTTClient("localhost", "esp32/output2", data_handler)
mqtt_client_3 = MQTTClient("localhost", "esp32/output3", data_handler)

# Lancer chaque client
mqtt_client_1.start()
mqtt_client_2.start()
mqtt_client_3.start()

db.create_tables()

@app.route('/start_session', methods=['POST'])
def start_session():
    if not data_handler.pause_session :
        session_name = request.form.get('session_name', 'Default Session')
        if session_name == "" :
            session_name = session_name = "Session_" + str(data_handler.get_last_session_id())
        data_handler.create_new_session(session_name)
        
    # Démarrer le client MQTT dans un thread séparé
    threading.Thread(target=mqtt_client_1.start).start()
    threading.Thread(target=mqtt_client_2.start).start()
    threading.Thread(target=mqtt_client_3.start).start()    

    return "Data collection started!"

@app.route('/pause_session', methods=['POST'])
def pause_session():
    # Logique pour mettre la session en pause (si nécessaire)
    data_handler.pause_session = True
    mqtt_client_1.stop()
    mqtt_client_2.stop()
    mqtt_client_3.stop()
    return "Session paused!"

@app.route('/stop_session', methods=['POST'])
def stop_session():
    mqtt_client_1.stop()
    mqtt_client_2.stop()
    mqtt_client_3.stop()
    data_handler.pause_session = False
    data_handler.close_session()
    return "Data collection stopped and session closed!"


def load_json_data() : 
    with open('action.json') as f :
        return json.load(f)

## Est-ce qu'il faut que je mette tout dans mon fichier json et que j'actualise à les moments donnés (par exemple toutes les 10 secondes) 
## ou  que dès qu'on actualise la page cela s'actualise (on perd l'utilisation du fichier json) ????????
@app.route('/api/update/dashboard', methods=['GET'])
def get_dashboard():
    data = load_json_data()  
    return jsonify(data)


# API pour récupérer les données en fonction du capteur sélectionné
@app.route('/api/data', methods=['GET'])
def get_data():
    sensor_type = request.args.get('sensor')  # Récupère le capteur sélectionné depuis le front-end
    session_id = request.args.get('session_id', None)  # Optionnel, si on veut filtrer par session

    # Dictionnaire pour mapper le capteur à la bonne table dans la base de données
    sensor_tables = {
        'sessions' : 'sessions',
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

    conn = get_db()
    conn.row_factory = sqlite3.Row  # Permet d'utiliser des noms de colonnes
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

