from Database import Database
import mqtt_client

def main() :
    
    # Collect the data with MQTT
        
    mqtt_client = MQTTClient("172.20.10.10", "esp32/output")