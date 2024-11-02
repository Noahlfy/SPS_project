<script setup>

import { handleError, ref } from 'vue';
import { getSessionId } from '@/services/apiServices';

const playButton = ref('Start');
const stopButton = ref('Stop');

const askSessionName = ref(false);
const sessionName = ref('Session')

const disablePlayButton = ref(false);
const disableStopButton = ref(true);

let status = 'completed';

const beginSession = () => {
    console.log('Name given.')
    askSessionName.value = false;

    fetch('http://localhost:8000/api/session/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "status": "active",
                "session_name": sessionName.value,
            }),
        })
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch((error) => console.error('Error:', error));   
};

const putStatusSession = async (status) => {
    try {
        const sessionId = await getSessionId(); // Attendre que la Promise soit résolue
        const response = await fetch(`http://localhost:8000/api/session/${sessionId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "status": status,
            }),
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        console.log('Success:', data);
    } catch (error) {
        console.error('Error updating session:', error);
    }
}

const startSession = () => {
    console.log('Session started, please give it a name')

    if (status === 'completed') {
        askSessionName.value = true;
        status = 'active';
        stopButton.value = 'Pause'
        disablePlayButton.value = true;
        disableStopButton.value = false;

    } else {
        putStatusSession("active");
        status = 'active';
        stopButton.value = 'Pause';
        playButton.value = 'Start';
        disablePlayButton.value = true;
        disableStopButton.value = false;

    }
}

const stopSession = () => {
    if (status === 'active') {
        putStatusSession("paused");
        console.log('Session Paused');
        status = 'paused';
        playButton.value = "Resume";
        stopButton.value = "End";
        disablePlayButton.value = false;
        disableStopButton.value = false;

    } else {
        putStatusSession("completed");
        console.log('Session completed');
        status = 'completed';
        playButton.value = "Start";
        stopButton.value = "Stop";
        disablePlayButton.value = false;
        disableStopButton.value = true;
        
    }
}


</script>

<template>
    <section>
        <div class="stats-container">
            <div class="buttons-display">
                <div class="buttons">
                    <button type="submit" id="play" @click="startSession" :disabled="disablePlayButton">
                        {{ playButton }}
                    </button>
                    <button type="submit" id="stop" @click="stopSession" :disabled="disableStopButton">
                        {{ stopButton }}
                    </button>
                </div>
                <div class="session-name">
                    <div v-if="askSessionName">
                        <input type="text" v-model="sessionName" placeholder="Session Name" @keyup.enter="beginSession"/>
                    </div>
                    <div v-else>
                        {{ sessionName }}
                    </div>
                </div>
            </div>
            <div class="player-stats">
                <div class="stats" id="distance">
                    <div class="stats-name">Distance</div>
                    <div class="stats-data">2.5km</div>
                </div>
                <div class="stats" id="fatigue-level">
                    <div class="stats-name">Fatigue Level</div>
                    <div class="stats-data">20%</div>
                </div>
                <div class="stats" id="position-quality">
                    <div class="stats-name">Position quality</div>
                    <div class="stats-data">90%</div>
                </div>
                <div class="stats" id="training-intensity">
                    <div class="stats-name">Training intensity</div>
                    <div class="stats-data">90%</div>
                </div>
                <div class="stats" id="concussion-risk">
                    <div class="stats-name">Concussion risk</div>
                    <div class="stats-data">3/5</div>
                </div>
            </div>
        </div>
    </section>
</template>