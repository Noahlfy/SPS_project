from Database import Database

if __name__ == "__main__":
    # Créer une instance de la base de données
    db = Database()

    # Insérer une session
    db.insert_session(1, '2024-09-24 10:00:00', '2024-09-24 11:00:00', 9.8, 5.0, 100.0, 1, 0.5)

    # Insérer des mesures pour la session
    db.insert_measurement(1, '2024-09-24 10:05:00', 0.1, 0.2, 0.3, 10.0, 20.0, 30.0)
    db.insert_measurement(1, '2024-09-24 10:10:00', 0.2, 0.3, 0.4, 15.0, 25.0, 35.0)

    # Récupérer toutes les sessions
    sessions = db.fetch_all_sessions()
    print("Sessions:", sessions)

    # Fermer la connexion à la base de données
    db.close()
