const sensorheader = {
    "sessions" : [ 'session_id', 'session_name', 'start_time', 'end_time', 'acceleration_max', 'speed_max', 'total_distance', 'commotion_risk', 'fatigue_level'],
    'BNO055_head':  ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
    'BNO055_chest': ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
    'BNO055_right_leg': ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
    'BNO055_left_leg': ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
    'BMP280': ['id', 'session_id', 'time', 'temperature', 'pressure'],
    'MAX30102': ['id', 'session_id', 'time', 'SpO2', 'BPM']
}

function updateTableColumns() {
    const sensor = document.getElementById('sensor-select');
    fetch('/api/data?sensor=' + sensor.value) 
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur réseau : ' + response.status)
            }
            return response.json();
    })
        .then(data => {
            console.log(data);
            const tableHeader = document.getElementById('tableHeader');
            tableHeader.innerHTML = '';

            sensorheader[sensor.value].forEach(column => {
                const th = document.createElement('th');
                th.textContent = column;
                tableHeader.appendChild(th);
            });

            const dataBody = document.getElementById('dataBody');
            dataBody.innerHTML = '';


            const numberOfRows = 25; // Nombre de lignes à afficher
            const rowsToDisplay = numberOfRows - data.length;

            data.forEach(row => {
                const tr = document.createElement('tr');
                sensorheader[sensor.value].forEach(column => {
                    const td = document.createElement('td');
                    td.textContent = row[column]; // Assure-toi d'utiliser la clé correcte
                    tr.appendChild(td);
                });
                dataBody.appendChild(tr); // N'oublie pas d'ajouter la ligne au corps du tableau
            });

            if (data.length < numberOfRows) {
                for (let i = data.length; i < rowsToDisplay; i++) {
                    const tr = document.createElement('tr');
                    sensorheader[sensor.value].forEach(() => {
                        const td = document.createElement('td');
                        td.textContent = ''; // Cellule vide
                        tr.appendChild(td);
                    });
                    dataBody.appendChild(tr);
                }
            }

        })
        .catch(error => {
            console.error('Erreur lors de la récupération des données :', error);
        });
}
                    
