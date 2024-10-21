# Classe pour gérer la connexion MQTT. Elle se chargera d'envoyer et de recevoir les données depuis l'ESP32.

import paho.mqtt.client as mqtt
import json
import subprocess

def start_mosquitto():
    # Commande pour démarrer Mosquitto avec la configuration appropriée
    mosquitto_command = r'mosquitto -c "C:\Program Files\mosquitto\mosquitto.conf" -v'

    # Si sous Windows, utilise `creationflags=subprocess.CREATE_NEW_CONSOLE` pour détacher le processus
    
    subprocess.Popen(mosquitto_command, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
       
    print("Mosquitto a été démarré en arrière-plan.")

# Appelle la fonction pour démarrer Mosquitto
start_mosquitto()


class MQTTClient:
    def __init__(self, broker_address, topic, data_handler):
        self.client = mqtt.Client(protocol=mqtt.MQTTv311)
        self.broker_address = broker_address
        self.topic = topic
        self.data_handler = data_handler

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
    def on_connect(self, client, userdata, flags, rc) :
        print("Connected with result code " + str(rc))
        client.subscribe(self.topic)
    
    def on_message(self, client, userdata, msg) :
        data = json.loads(msg.payload.decode())        
        self.data_handler.process_data(data)

                
    def start(self):
        self.client.connect(self.broker_address, 1883, 60)
        self.client.loop_start()  # Utilisation de loop_start pour éviter un blocage

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        

