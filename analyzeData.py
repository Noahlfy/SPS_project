import json
import os

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
                    

convertJsonData()
# def accelerationNorm() :
    
# def distance() :
    
# def distanceNorm() : 
    
        
# def speed() :
# def speedNorm() :