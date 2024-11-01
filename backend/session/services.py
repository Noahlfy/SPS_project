from django.conf import settings
import threading
from multiprocessing import Process

from backend.mqqt_client import MQTTClient
from backend.data_handler import DataHandler
from backend.database import Database

db = Database(settings.DATABASES['default']['NAME'])
data_handler = DataHandler(db)

mqtt_client_1 = MQTTClient("localhost", "esp32/output1", data_handler)
mqtt_client_2 = MQTTClient("localhost", "esp32/output2", data_handler)
mqtt_client_3 = MQTTClient("localhost", "esp32/output3", data_handler)

def start_mqtt_clients(session_id):
    data_handler.active_session_id = session_id
    threading.Thread(target=mqtt_client_1.start, daemon=True).start()
    threading.Thread(target=mqtt_client_2.start, daemon=True).start()
    threading.Thread(target=mqtt_client_3.start, daemon=True).start()

def stop_mqtt_clients():
    mqtt_client_1.stop()
    mqtt_client_2.stop()
    mqtt_client_3.stop()

def close_mqtt_clients():
    mqtt_client_1.stop()
    mqtt_client_2.stop()
    mqtt_client_3.stop()
    data_handler.close_session()