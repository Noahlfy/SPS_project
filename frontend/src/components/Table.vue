<script setup>

import { ref, onMounted, watch} from 'vue';

const sensorheader = {
    "raw data" : {
        "session" : [ 'session_id', 'session_name', 'start_time', 'end_time', 'acceleration_max', 'speed_max', 'total_distance', 'concussion_risk', 'fatigue_level'],
        'head':  ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
        'chest': ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
        'right-leg': ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
        'left-leg': ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
        'temperature': ['id', 'session_id', 'time', 'temperature', 'pressure'],
        'heart-rate': ['id', 'session_id', 'time', 'SpO2', 'BPM']
    },
    "transformed data" :  {
        'head':  ['session_id', 'timestamp', 'accel_x', 'accel_y', 'accel_z', 'vel_x', 'vel_y', 'vel_z', 'pos_x', 'pos_y', 'pos_z'],
        'chest': ['session_id', 'timestamp', 'accel_x', 'accel_y', 'accel_z', 'vel_x', 'vel_y', 'vel_z', 'pos_x', 'pos_y', 'pos_z'],
        'right-leg': ['session_id', 'timestamp', 'accel_x', 'accel_y', 'accel_z', 'vel_x', 'vel_y', 'vel_z', 'pos_x', 'pos_y', 'pos_z'],
        'left-leg': ['session_id', 'timestamp', 'accel_x', 'accel_y', 'accel_z', 'vel_x', 'vel_y', 'vel_z', 'pos_x', 'pos_y', 'pos_z']
    }
}

const selectedSensor = ref('session');
const selectedDataType = ref('raw');
const columns = ref([]);
const rows = ref([]);

const fetchData = async (sensor, dataType) => {
    try {
        const response = await fetch(`http://localhost:8000/api/${sensor}/`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error; // Relance l'erreur pour la gestion ultérieure
        return []
    }
};

const updateTableColumns = async () => {
    const dataType = selectedDataType.value === 'raw' ? 'raw data' : 'transformed data';
    columns.value = sensorheader[dataType][selectedSensor.value];
    
    // Exemple de récupération de données (à adapter selon votre logique)
    // Remplacez cette ligne par une fonction qui charge vos données
    rows.value = await fetchData(selectedSensor.value, dataType); 
};

watch(selectedSensor, updateTableColumns);
watch(selectedDataType, updateTableColumns);

onMounted(updateTableColumns);

</script>

<template>
    <section>
    <div class="sensor-selection">
        <select id="sensor-select"  v-model="selectedSensor">
            <option value="session">session</option>
            <option value="head">Head BNO055</option>
            <option value="chest">Chest BNO055</option>
            <option value="right-leg">Right Leg BNO055</option>
            <option value="left-leg">Left Leg BNO055</option>
            <option value="heart-rate">heart-rate</option>
            <option value="temperature">temperature</option>
        </select>
        <select id="data-type" class="data-type" v-model="selectedDataType"> 
            <option value="raw">Raw</option>
            <option value="transformed">Transformed</option>
        </select>
    </div>

    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th v-for="column in columns" :key="column">{{ column }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="row in rows" :key="row.id">
                    <td v-for="column in columns" :key="column">{{ row[column] }}</td>
                </tr>
            </tbody>
        </table>
    </div>
    </section>

</template>