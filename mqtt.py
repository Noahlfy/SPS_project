import paho.mqtt.client as mqtt
import json
import os
import subprocess
import sys
import io

folder_path = "Data"

time_data = []
accel_x_data = []
accel_y_data = []
accel_z_data = []
 
eul_x_data = []
eul_y_data = []
eul_z_data = []

t = 0
time_step = 0.5

# Fonction appelée lors de la connexion à Mosquitto
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # S'abonner au topic où sont publiées les données
    client.subscribe("esp32/output")

# Fonction appelée lorsqu'un message est reçu
def on_message(client, userdata, msg):
    global t
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    
    # Conversion du message en JSON
    data = json.loads(msg.payload.decode())
    
    time_data.append(t)
    accel_x_data.append(data['accel_x'])
    accel_y_data.append(data['accel_y'])
    accel_z_data.append(data['accel_z'])
    
    eul_x_data.append(data['eul_x'])
    eul_y_data.append(data['eul_y'])
    eul_z_data.append(data['eul_z'])
    
    t += time_step  # Incrément du temps

    
    print(f"Accelerometer X: {data['accel_x']}, Y: {data['accel_y']}, Z: {data['accel_z']}")
    print(f"Euler X: {data['eul_x']}, Y: {data['eul_y']}, Z: {data['eul_z']}")

    # Exemple de traitement simple
    if data['accel_x'] > 10:
        print("Alert: High acceleration detected!")

    file_path = os.path.join(folder_path, "data_test.json")

    # Lire les données existantes si le fichier existe
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            try:
                existing_data = json.load(json_file)
            except json.JSONDecodeError:
                existing_data = []  # Si le fichier est vide ou corrompu, initialiser à une liste vide
    else:
        existing_data = []  # Si le fichier n'existe pas encore, commencer avec une liste vide

    # Ajouter les nouvelles données aux données existantes
    existing_data.append(data)

    # Écrire toutes les données (anciennes + nouvelles) dans le fichier
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


# Démarrer mosquitto

captured_output = io.StringIO()
sys.stdout = captured_output

# Vérifie si Mosquitto est en cours d'exécution
command = r'tasklist | findstr mosquitto'
subprocess.run(command, shell=True)

# Récupère la sortie capturée
output = captured_output.getvalue()
captured_output.close()
sys.stdout = sys.__stdout__  # Restaure stdout à son état d'origine

# Vérifie si Mosquitto est dans la sortie
if "mosquitto.exe" in output:
    print("Mosquitto est déjà en cours d'exécution.")
else:
    print("Mosquitto n'est pas en cours d'exécution. Tentative de démarrage...")
    # Démarre Mosquitto
    command = r'mosquitto -c "C:\Program Files\mosquitto\mosquitto.conf" -v'
    mosquitto_process = subprocess.Popen(command, shell=True)
    
    
# Configuration du client MQTT
client = mqtt.Client(protocol=mqtt.MQTTv311)  # Utiliser MQTT v3.1.1
client.on_connect = on_connect
client.on_message = on_message

# Connexion au broker Mosquitto
client.connect("172.20.10.10", 1883, 60)

# Démarrage de la boucle pour écouter les messages
client.loop_forever()
