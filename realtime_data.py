from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import sqlite3
import pandas as pd
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Fonction pour récupérer des données depuis SQLite
def get_data_from_db():
    conn = sqlite3.connect('Database.db')
    query = "SELECT * FROM measurements"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient='records')

# Route classique pour récupérer les données
@app.route('/api/data', methods=['GET'])
def send_data():
    data = get_data_from_db()
    return jsonify(data)

# Émission de données en temps réel via Socket.IO
@socketio.on('request_data')
def send_realtime_data():
    while True:
        data = get_data_from_db()  # Récupère les données à partir de la base
        emit('update_data', data)  # Envoie les données au client
        socketio.sleep(5)  # Envoie des données toutes les 5 secondes

if __name__ == '__main__':
    socketio.run(app, debug=True)
