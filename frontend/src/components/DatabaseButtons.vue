<script setup>

const sensorheader = {
    "sessions" : [ 'session_id', 'session_name', 'start_time', 'end_time', 'acceleration_max', 'speed_max', 'total_distance', 'concussion_risk', 'fatigue_level'],
    'BNO055_head':  ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
    'BNO055_chest': ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
    'BNO055_right_leg': ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
    'BNO055_left_leg': ['id', 'session_id', 'time', 'accel_x', 'accel_y', 'accel_z', 'quat_w', 'quat_x', 'quat_y', 'quat_z'],
    'BMP280': ['id', 'session_id', 'time', 'temperature', 'pressure'],
    'MAX30102': ['id', 'session_id', 'time', 'SpO2', 'BPM']
};

const sensorSelect = 'sessions';

</script>

<template>
    <div class="sensor-selection">
        <select id="sensor-select"  onchange="updateTableColumns()">
            <option value="sessions">Sessions</option>
            <option value="BNO055_head">Head BNO055</option>
            <option value="BNO055_chest">Chest BNO055</option>
            <option value="BNO055_right_leg">Right Leg BNO055</option>
            <option value="BNO055_left_leg">Left Leg BNO055</option>
            <option value="MAX30102">MAX30102</option>
            <option value="BMP280">BMP280</option>
        </select>
        <select id="data-type" class="data-type" onchange="updateTableColumns()"> 
            <option value="raw">Raw</option>
            <option value="transformed">Transformed</option>
        </select>
    </div>
</template>