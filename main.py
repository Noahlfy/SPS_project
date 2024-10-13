from Database import Database
from mqtt_client import MQTTClient
from data_handler import DataHandler
from stats_calculator import RealTimeStatistics
# from stats_calculator import RealTimePlotter

def main() :
    
    # Collect the data with MQTT
    db = Database("database.db")
    data_handler = DataHandler(db)
    mqtt_client = MQTTClient("172.20.10.10", "esp32/output", data_handler)
    
    mqtt_client.start()
    db.create_tables()
    try:
        while True:
            command = input("Tape 'new' pour démarrer une nouvelle session, 'stop' pour arrêter la session actuelle, ou 'exit' pour quitter : ").strip()
            if command == "new":
                command2 = input("Write the name you want to want to give or None")
                if not command2 :
                    data_handler.create_new_session("Session_" + str(data_handler.get_last_session_id()))
                else :
                    data_handler.create_new_session(command2)
                print("New session started.")
                
                show_stats = RealTimeStatistics(db)
                show_stats.pace()
                
            elif command == "stop":
                data_handler.close_session()
                print("Session ended.")
            elif command == "exit":
                break
            print("Sessions: ", db.fetch_all_sessions())
            print("Measurements: ", db.fetch_all_measurements())
    except KeyboardInterrupt:
        print("Interruption par l'utilisateur.")
        
    mqtt_client.stop()

main()

