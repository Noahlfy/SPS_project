import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def convertJsonData () : 
    path_import = 'Data_test1'
    path_export = 'Data.json'
    
    files_names = [f for f in os.listdir(path_import) if os.path.isfile(os.path.join(path_import, f))]
    print(files_names)
    for name in files_names :
        with open(path_import + '/' + name) as f :
            data = json.load(f)
        all_data = {}
        for e in data : 
            for (key, value) in e.items() :
                if key not in all_data :
                    all_data[key] = []
                all_data[key].append(value)
        file_path = os.path.join(path_export, name)
        with open(file_path, 'w') as json_file :
                json.dump(all_data, json_file, indent=4)
                    


def accelerationNorm(path, file_name) :
    with open(path + "/" + file_name + ".json") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['accel_norm'] = np.sqrt(df['accel_x']**2 + df['accel_y']**2 + df['accel_z']**2)
    print(df)
    plt.figure(figsize=(10, 6))
    plt.plot(df['Time'], df['accel_norm'], label='Norme de l\'accélération', color='b', marker='o')

    # Ajouter des labels et un titre
    plt.title('Norme de l\'accélération en fonction du temps', fontsize=14)
    plt.xlabel('Temps (s)', fontsize=12)
    plt.ylabel('Norme de l\'accélération (m/s²)', fontsize=12)

    # Activer la grille
    plt.grid(True)
    # Afficher la légende
    plt.legend()

    # Afficher le graphique
    plt.show()
    
accelerationNorm("Data.json", "data_test1")
# def distance() :
    
# def distanceNorm() : 
    
        
# def speed() :
# def speedNorm() :