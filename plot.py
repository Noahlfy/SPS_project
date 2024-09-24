import matplotlib.pyplot as plt
import json
import math

path = "Data"

def plot(name) : 
    with open(path + "/" + name + ".json") as f :
        data = json.load(f)
    time = []
    all_data  = {}
    t = 0
    for element in data : 
        for key, value in element.items() : 
            if key not in all_data : 
                all_data[key] = []
            all_data[key].append(value)
        time.append(t)
        t += 0.500

    num_graphs = len(all_data)
    num_cols = 3
    num_rows = math.ceil(num_graphs/num_cols)
    
    
    
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(12, num_rows * 3))  # Taille adaptée

    axs = axs.flatten()  
    
    for i, (key, values) in enumerate(all_data.items()):
        axs[i].plot(time, values, label=key)
        axs[i].set_xlabel('Temps (s)')
        axs[i].set_ylabel(key)
        axs[i].legend()

    for j in range(i + 1, len(axs)):
        fig.delaxes(axs[j])

    plt.tight_layout()  
    plt.show()
    return None

plot("data1")