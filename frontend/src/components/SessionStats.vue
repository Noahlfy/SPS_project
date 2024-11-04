<script setup>
import { ref, computed, watch } from 'vue';
import { useDataStore } from '@/stores/dataStore';

const dataStore = useDataStore();

const playButton = ref('Start');
const stopButton = ref('Stop');

const askSessionName = ref(false);
const sessionName = ref('Session');

const disablePlayButton = ref(false);
const disableStopButton = ref(true);


const currentSession = computed(() => {
  const sessions = dataStore.session || [];
  
  // Prioriser la session active
  let activeSession = sessions.find(session => session.status !== 'completed');
  if (activeSession) {
    // Vous pouvez effacer 'selectedSessionId' si vous souhaitez que la session active prenne toujours le dessus
    dataStore.selectedSessionId = activeSession.session_id;
    return activeSession;
  }
  
  // Si une session est sélectionnée, l'utiliser
  if (dataStore.selectedSessionId) {
    return sessions.find(session => session.session_id === dataStore.selectedSessionId) || null;
  }
  
  // Sinon, retourner la dernière session
  if (sessions.length > 0) {
    return sessions[sessions.length - 1];
  } else {
    return null;
  }
});



const status = computed(() => {
    console.log('Calcul de status...');

  return currentSession.value ? currentSession.value.status : 'completed';
});

const putStatusSession = async (statusToUpdate) => {
  try {
    if (!currentSession.value) {
      console.error('No active session to update.');
      return;
    }
    const sessionId = currentSession.value.session_id;

    // Requête PUT pour mettre à jour le statut
    const response = await fetch(`http://localhost:8000/api/session/${sessionId}/`, {
      method: 'PUT', // ou 'PATCH' si votre API le permet
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "status": statusToUpdate,
      }),
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      console.error('Erreur lors de la mise à jour de la session :', errorData);
      throw new Error('Network response was not ok');
    }
    
    const updatedSession = await response.json();
    console.log('Succès de la mise à jour de la session :', updatedSession);

    // Requête GET pour récupérer les sessions mises à jour
    const sessionsResponse = await fetch('http://localhost:8000/api/session/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!sessionsResponse.ok) {
      const errorData = await sessionsResponse.json();
      console.error('Erreur lors de la récupération des sessions :', errorData);
      throw new Error('Network response was not ok');
    }

    const sessionsData = await sessionsResponse.json();
    console.log('Sessions récupérées :', sessionsData);

    // Mettre à jour dataStore.session avec les nouvelles données
    dataStore.updateData('session', sessionsData);

    // Le 'watch' sur 'status' se déclenchera automatiquement

  } catch (error) {
    console.error('Error in putStatusSession:', error);
  }
};


const updateButtonStates = () => {
  if (status.value === 'active') {
    playButton.value = 'Start';
    stopButton.value = 'Pause';
    disablePlayButton.value = true;
    disableStopButton.value = false;
  } else if (status.value === 'paused') {
    playButton.value = 'Resume';
    stopButton.value = 'End';
    disablePlayButton.value = false;
    disableStopButton.value = false;
  } else if (status.value === 'completed') {
    playButton.value = 'Start';
    stopButton.value = 'Stop';
    disablePlayButton.value = false;
    disableStopButton.value = true;
  }
};

const startSession = () => {
  console.log('Start button clicked');

  if (status.value === 'completed') {
    askSessionName.value = true;
    disablePlayButton.value = true;
    disableStopButton.value = true;
  } else if (status.value === 'paused') {
    // Reprendre la session
    putStatusSession('active');
  }
};

const stopSession = () => {
  console.log('Stop button clicked');

  if (status.value === 'active') {
    // Mettre la session en pause
    putStatusSession('paused');
  } else if (status.value === 'paused') {
    // Terminer la session
    putStatusSession('completed');
  }
};


watch(
  status,
  (newVal, oldVal) => {
    console.log(`Le statut a changé de ${oldVal} à ${newVal}`);
    updateButtonStates();
  },
  { immediate: true }
);


const displayedSessionName = computed(() => {
  if (askSessionName.value) {
    return sessionName.value;
  } else if (currentSession.value) {
    return currentSession.value.session_name;
  } else {
    return 'Session';
  }
});


const beginSession = async () => {
  try {
    console.log('Session name given:', sessionName.value);
    askSessionName.value = false;

    // Créer une nouvelle session via une requête POST
    const response = await fetch('http://localhost:8000/api/session/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "status": "active",
        "session_name": sessionName.value,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Erreur lors de la création de la session :', errorData);
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    console.log('Session créée avec succès :', data);

    // Requête GET pour récupérer les sessions mises à jour
    const sessionsResponse = await fetch('http://localhost:8000/api/session/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!sessionsResponse.ok) {
      const errorData = await sessionsResponse.json();
      console.error('Erreur lors de la récupération des sessions :', errorData);
      throw new Error('Network response was not ok');
    }

    const sessionsData = await sessionsResponse.json();
    console.log('Sessions récupérées :', sessionsData);

    // Mettre à jour dataStore.session avec les nouvelles données
    dataStore.updateData('session', sessionsData);

    // Le 'watch' sur 'status' se déclenchera automatiquement
    // Les boutons seront mis à jour via le watch sur 'status'

  } catch (error) {
    console.error('Erreur dans beginSession:', error);
  }
};

const latestSessionStats = computed(() => {
  const stats = dataStore['session-stats'] || [];
  if (!currentSession.value) {
    return null;
  }
  const currentSessionId = currentSession.value.session_id;
  // Vérifiez si stat.session_id est un nombre ou un objet
  const currentSessionStats = stats.filter(stat => {
    if (typeof stat.session_id === 'object' && stat.session_id !== null) {
      return stat.session_id.session_id === currentSessionId;
    } else {
      return stat.session_id === currentSessionId;
    }
  });
  if (currentSessionStats.length === 0) {
    return null;
  }
  // Retourner la dernière stat
  return currentSessionStats[currentSessionStats.length - 1];
});

const distanceDisplay = computed(() => {
  if (latestSessionStats.value && latestSessionStats.value.distance !== null) {
    return `${latestSessionStats.value.distance.toFixed(2)} km`;
  } else {
    return 'N/A';
  }
});

const fatigueLevelDisplay = computed(() => {
  if (latestSessionStats.value && latestSessionStats.value.fatigue_level !== null) {
    return `${(latestSessionStats.value.fatigue_level * 100).toFixed(0)}%`;
  } else {
    return 'N/A';
  }
});

const positionQualityDisplay = computed(() => {
  if (latestSessionStats.value && latestSessionStats.value.footing_quality !== null) {
    return `${(latestSessionStats.value.footing_quality * 100).toFixed(0)}%`;
  } else {
    return 'N/A';
  }
});

const trainingIntensityDisplay = computed(() => {
  if (latestSessionStats.value && latestSessionStats.value.training_intensity !== null) {
    return `${(latestSessionStats.value.training_intensity * 100).toFixed(0)}%`;
  } else {
    return 'N/A';
  }
});

const concussionRiskDisplay = computed(() => {
  if (latestSessionStats.value && latestSessionStats.value.concussion_risk !== null) {
    return `${(latestSessionStats.value.concussion_risk).toFixed(1)}/5`;
  } else {
    return 'N/A';
  }
});
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
            {{ displayedSessionName }}
          </div>
        </div>
      </div>
      <div class="player-stats">
        <div class="stats" id="distance">
          <div class="stats-name">Distance</div>
          <div class="stats-data">{{ distanceDisplay }}</div>
        </div>
        <div class="stats" id="fatigue-level">
          <div class="stats-name">Fatigue Level</div>
          <div class="stats-data">{{ fatigueLevelDisplay }}</div>
        </div>
        <div class="stats" id="position-quality">
          <div class="stats-name">Position quality</div>
          <div class="stats-data">{{ positionQualityDisplay }}</div>
        </div>
        <div class="stats" id="training-intensity">
          <div class="stats-name">Training intensity</div>
          <div class="stats-data">{{ trainingIntensityDisplay }}</div>
        </div>
        <div class="stats" id="concussion-risk">
          <div class="stats-name">Concussion risk</div>
          <div class="stats-data">{{ concussionRiskDisplay }}</div>
        </div>
      </div>
    </div>
  </section>
</template>
