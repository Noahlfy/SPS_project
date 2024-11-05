<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useDataStore } from '@/stores/dataStore';
import { Chart, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns';

// Enregistrer les composants Chart.js
Chart.register(...registerables);

const dataStore = useDataStore();

const currentSession = computed(() => {
  const sessions = dataStore.session || [];

  // Prioriser la session active
  let activeSession = sessions.find(session => session.status !== 'completed');
  if (activeSession) {
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

// Filtrer les données des statistiques pour la session actuelle
const sessionStats = computed(() => {
  const stats = dataStore['session-stats'] || [];
  if (!currentSession.value) {
    return [];
  }
  const currentSessionId = currentSession.value.session_id;
  // Filtrer les stats pour la session actuelle
  return stats.filter(stat => stat.session_id === currentSessionId);
});

// Références aux éléments canvas
const paceChartRef = ref(null);
const gChartRef = ref(null);
const heartRateChartRef = ref(null);

// Instances des graphiques
let paceChartInstance = null;
let gChartInstance = null;
let heartRateChartInstance = null;

// Fonction pour créer les données du graphique
const createChartData = (label, dataKey, color) => {
  return {
    labels: sessionStats.value.map(item => new Date(item.time)), // Utiliser des objets Date
    datasets: [
      {
        label: label,
        data: sessionStats.value.map(item => item[dataKey]),
        borderColor: color,
        backgroundColor: color,
        fill: false,
      },
    ],
  };
};

// Fonction pour créer les options du graphique
const createChartOptions = () => {
  return {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        type: 'time', // Utiliser l'échelle de temps
        time: {
          unit: 'second', // Ajuster l'unité de temps si nécessaire
          displayFormats: {
            second: 'HH:mm:ss',
            minute: 'HH:mm',
          },
        },
        ticks: {
          autoSkip: true,
          maxTicksLimit: 10,
        },
      },
      y: {
        beginAtZero: true,
      },
    },
  };
};

// Fonction pour initialiser les graphiques
const initializeCharts = () => {
  // Vérifier que les références canvas sont disponibles
  if (!paceChartRef.value || !gChartRef.value || !heartRateChartRef.value) {
    return;
  }

  // Pace Chart
  const paceCtx = paceChartRef.value.getContext('2d');
  paceChartInstance = new Chart(paceCtx, {
    type: 'line',
    data: createChartData('Pace (km/h)', 'pace', 'rgba(75, 192, 192, 1)'),
    options: createChartOptions(),
  });

  // G Chart
  const gCtx = gChartRef.value.getContext('2d');
  gChartInstance = new Chart(gCtx, {
    type: 'line',
    data: createChartData('G-force (g)', 'g', 'rgba(255, 99, 132, 1)'),
    options: createChartOptions(),
  });

  // Heart Rate Chart
  const heartRateCtx = heartRateChartRef.value.getContext('2d');
  heartRateChartInstance = new Chart(heartRateCtx, {
    type: 'line',
    data: createChartData('Heart Rate (BPM)', 'BPM', 'rgba(54, 162, 235, 1)'),
    options: createChartOptions(),
  });
};

watch(sessionStats, (newValue) => {
  const timestamps = newValue.map(item => new Date(item.time));
  const timestampsInMs = timestamps.map(t => t.getTime());

  if (paceChartInstance) {
    paceChartInstance.data.labels = timestamps;
    paceChartInstance.data.datasets[0].data = newValue.map(item => item.pace);
    paceChartInstance.update();
  }

  if (gChartInstance) {
    gChartInstance.data.labels = timestamps;
    gChartInstance.data.datasets[0].data = newValue.map(item => item.g);
    gChartInstance.update();
  }

  if (heartRateChartInstance) {
    const bpmData = newValue.map(item => item.BPM).filter(bpm => bpm !== null && bpm !== undefined);

    if (bpmData.length > 0) {
      heartRateChartInstance.data.labels = timestamps;
      heartRateChartInstance.data.datasets[0].data = bpmData;
      heartRateChartInstance.options.scales.x.min = timestampsInMs[0];
      heartRateChartInstance.options.scales.x.max = timestampsInMs[timestampsInMs.length - 1];
      heartRateChartInstance.update();
    } else {
      console.warn("BPM data is missing or invalid.");
    }
  }
}, { immediate: true });


// Observer les changements dans les références des canvas et initialiser les graphiques
watch([paceChartRef, gChartRef, heartRateChartRef], ([newPaceRef, newGRef, newHeartRateRef]) => {
  if (newPaceRef && newGRef && newHeartRateRef) {
    initializeCharts();
  }
}, { immediate: true });

</script>

<template>
  <section>
    <div class="graphics-container">
      <div class="graph" id="pace">
        <canvas id="paceChart" ref="paceChartRef"></canvas>
      </div>
      <div class="graph" id="g">
        <canvas id="gChart" ref="gChartRef"></canvas>
      </div>
      <div class="graph" id="heart-rate">
        <canvas id="heartRateChart" ref="heartRateChartRef"></canvas>
      </div>
    </div>
  </section>
</template>
