<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useDataStore } from '@/stores/dataStore';
import { Chart, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns'; // Import the date adapter for Chart.js
import { data } from 'autoprefixer';

// Register Chart.js components
Chart.register(...registerables);

const dataStore = useDataStore();


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


// Filtrer les données des statistiques pour la session actuelle
const sessionStats = computed(() => {
  const stats = dataStore['session-stats'] || [];
  if (!currentSession.value) {
    return [];
  }
  const currentSessionId = currentSession.value.session_id;
  // Filtrer les stats pour la session actuelle
  console.log(currentSessionId)
  console.log(dataStore['session-stats'])
  console.log("stats:", JSON.stringify(stats.filter(stat => stat.session_id_id === currentSessionId), null, 2));

  return stats.filter(stat => stat.session_id_id === currentSessionId);
});

// References to canvas elements
const paceChartRef = ref(null);
const gChartRef = ref(null);
const heartRateChartRef = ref(null);

// Chart instances
let paceChartInstance = null;
let gChartInstance = null;
let heartRateChartInstance = null;

// Function to create chart data
const createChartData = (label, dataKey, color) => {
  return {
    labels: sessionStats.value.map(item => new Date(item.time)), // Use Date objects
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

// Function to create chart options
const createChartOptions = () => {
  return {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        type: 'time', // Use the time scale
        time: {
          unit: 'second', // Adjust the time unit as needed (second, minute, hour)
          displayFormats: {
            second: 'HH:mm:ss',
            minute: 'HH:mm',
          },
        },
        min: (context) => {
          // Limite inférieure dynamique, ici -5 minutes du dernier point
          const timestamps = sessionStats.value.map(item => new Date(item.time));
          return timestamps.length > 0
            ? new Date(Math.max(...timestamps) - 5 * 60 * 1000)
            : null;
        },
        max: (context) => {
          // Limite supérieure dynamique (date actuelle)
          const timestamps = sessionStats.value.map(item => new Date(item.time));
          return timestamps.length > 0 ? Math.max(...timestamps) : null;
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

// Function to initialize charts
const initializeCharts = () => {
  // Pace Chart
  const paceCtx = paceChartRef.value.getContext('2d');
  paceChartInstance = new Chart(paceCtx, {
    type: 'line',
    data: createChartData('Pace (min/km)', 'pace', 'rgba(75, 192, 192, 1)'),
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

// Watch for changes in sessionStats and update charts
watch(sessionStats, (newValue) => {
  const timestamps = newValue.map(item => new Date(item.time));

  if (paceChartInstance) {
    paceChartInstance.data.labels = timestamps;
    paceChartInstance.data.datasets[0].data = newValue.map(item => item.pace);
    paceChartInstance.options.scales.x.min = timestamps.length > 0
      ? new Date(Math.max(...timestamps) - 5 * 60 * 1000)
      : null;
    paceChartInstance.options.scales.x.max = timestamps.length > 0
      ? Math.max(...timestamps)
      : null;
    paceChartInstance.update();
  }

  if (gChartInstance) {
    gChartInstance.data.labels = timestamps;
    gChartInstance.data.datasets[0].data = newValue.map(item => item.g);
    gChartInstance.options.scales.x.min = timestamps.length > 0
      ? new Date(Math.max(...timestamps) - 5 * 60 * 1000)
      : null;
    gChartInstance.options.scales.x.max = timestamps.length > 0
      ? Math.max(...timestamps)
      : null;
    gChartInstance.update();
  }

  if (heartRateChartInstance) {
    heartRateChartInstance.data.labels = timestamps;
    heartRateChartInstance.data.datasets[0].data = newValue.map(item => item.BPM);
    heartRateChartInstance.options.scales.x.min = timestamps.length > 0
      ? new Date(Math.max(...timestamps) - 5 * 60 * 1000)
      : null;
    heartRateChartInstance.options.scales.x.max = timestamps.length > 0
      ? Math.max(...timestamps)
      : null;
    heartRateChartInstance.update();
  }
}, { immediate: true });


onMounted(() => {
  initializeCharts();
});
</script>

<template>
  <section>
    <div class="graphics-container">
      <div class="graph" id="pace">
        <canvas id="myChart" ref="paceChartRef"></canvas>
      </div>
      <div class="graph" id="g">
        <canvas id="myChart" ref="gChartRef"></canvas>
      </div>
      <div class="graph" id="heart-rate">
        <canvas id="myChart" ref="heartRateChartRef"></canvas>
      </div>
    </div>
  </section>
</template>
