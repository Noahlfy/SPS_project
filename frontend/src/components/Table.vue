<script setup>
import { ref, computed } from 'vue';
import { useDataStore } from '@/stores/dataStore';

const dataStore = useDataStore();

const sensorheader = {
  raw: {
    session: ['session_id', 'session_name', 'start_time', 'end_time'],
    head: ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
    chest: ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
    'right-leg': ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
    'left-leg': ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
    temperature: ['id', 'session_id', 'time', 'temperature', 'pressure'],
    'heart-rate': ['id', 'session_id', 'time', 'SpO2', 'BPM'],
    'session-stats': [],
  },
  transformed: {
    'head-transformed': ['session_id', 'timestamp', 'accel_x', 'accel_y', 'accel_z', 'vel_x', 'vel_y', 'vel_z', 'pos_x', 'pos_y', 'pos_z'],
    'chest-transformed': ['session_id', 'timestamp', 'accel_x', 'accel_y', 'accel_z', 'vel_x', 'vel_y', 'vel_z', 'pos_x', 'pos_y', 'pos_z'],
    'right-leg-transformed': ['session_id', 'timestamp', 'accel_x', 'accel_y', 'accel_z', 'vel_x', 'vel_y', 'vel_z', 'pos_x', 'pos_y', 'pos_z'],
    'left-leg-transformed': ['session_id', 'timestamp', 'accel_x', 'accel_y', 'accel_z', 'vel_x', 'vel_y', 'vel_z', 'pos_x', 'pos_y', 'pos_z'],
  },
};

const selectedSensor = ref('session');
const selectedDataType = ref('raw');

const transformable = ['head', 'chest', 'right-leg', 'left-leg'];

// Propriété calculée pour les colonnes
const columns = computed(() => {
  const dataType = selectedDataType.value;
  const sensor = selectedSensor.value;

  if (dataType === 'transformed' && transformable.includes(sensor)) {
    return sensorheader[dataType][`${sensor}-transformed`];
  } else {
    return sensorheader[dataType][sensor];
  }
});

// Propriété calculée pour les lignes
const rows = computed(() => {
  const dataType = selectedDataType.value;
  let sensor = selectedSensor.value;

  if (transformable.includes(sensor) && dataType === 'transformed') {
    sensor = `${sensor}-transformed`;
  }

  return dataStore[sensor];
});

</script>

<template>
  <section>
    <div class="sensor-selection">
      <select id="sensor-select" v-model="selectedSensor">
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
            <td v-for="column in columns" :key="column">
              {{ typeof row[column] === 'number' ? row[column].toFixed(2) : row[column] }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
