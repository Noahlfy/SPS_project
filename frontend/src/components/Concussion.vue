<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useDataStore } from '@/stores/dataStore';
import { Chart, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns';

Chart.register(...registerables);

const dataStore = useDataStore();

// Sessions Data
const sessions = computed(() => dataStore.session || []);
const selectedSessionId = computed({
  get: () => dataStore.selectedSessionId,
  set: (value) => {
    dataStore.selectedSessionId = value;
  },
});

const currentSession = computed(() => {
  const sessionsList = sessions.value;
  if (selectedSessionId.value) {
    return sessionsList.find(session => session.session_id === selectedSessionId.value) || null;
  }
  let activeSession = sessionsList.find(session => session.status !== 'completed');
  return activeSession || (sessionsList.length > 0 ? sessionsList[sessionsList.length - 1] : null);
});

// Fetching Stats Data
const concussionStats = computed(() => {
  const stats = dataStore['concussion-stats'] || [];
  if (!currentSession.value) return [];
  const currentSessionId = currentSession.value.session_id;
  return stats.filter(stat => stat.session_id === currentSessionId);
});

const sessionStats = computed(() => {
  const stats = dataStore['session-stats'] || [];
  if (!currentSession.value) return [];
  const currentSessionId = currentSession.value.session_id;
  return stats.filter(stat => stat.session_id === currentSessionId);
});

const latestConcussionStat = computed(() => {
  return concussionStats.value.length > 0 ? concussionStats.value[concussionStats.value.length - 1] : null;
});

const latestSessionStat = computed(() => {
  return sessionStats.value.length > 0 ? sessionStats.value[sessionStats.value.length - 1] : null;
});

// Chart Refs
const footingQualityChartRef = ref(null);
const spO2ChartRef = ref(null);
const BPMChartRef = ref(null);
const gChartRef = ref(null);

// Chart Instances
let footingQualityChartInstance = null;
let spO2ChartInstance = null;
let BPMChartInstance = null;
let gChartInstance = null;

// Create Chart Data
const createChartData = (label, dataKey, color, dataSource = 'concussion-stats') => {
  const data = dataSource === 'session-stats' ? sessionStats.value : concussionStats.value;
  return {
    labels: data.map(item => new Date(item.time)),
    datasets: [
      {
        label: label,
        data: data.map(item => item[dataKey]),
        borderColor: color,
        backgroundColor: color,
        fill: false,
      },
    ],
  };
};

// Chart Options
const createChartOptions = () => {
  return {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'second',
          displayFormats: { second: 'HH:mm:ss', minute: 'HH:mm' },
        },
        ticks: { autoSkip: true, maxTicksLimit: 10 },
      },
      y: { beginAtZero: true },
    },
  };
};

// Initialize or Update Charts
const initializeOrUpdateCharts = () => {
  // Destroy existing charts if they exist
  if (footingQualityChartInstance) footingQualityChartInstance.destroy();
  if (spO2ChartInstance) spO2ChartInstance.destroy();
  if (BPMChartInstance) BPMChartInstance.destroy();
  if (gChartInstance) gChartInstance.destroy();

  // Recreate charts
  if (footingQualityChartRef.value) {
    const ctx = footingQualityChartRef.value.getContext('2d');
    footingQualityChartInstance = new Chart(ctx, {
      type: 'line',
      data: createChartData('Footing Quality', 'footing_quality', 'rgba(75, 192, 192, 1)'),
      options: createChartOptions(),
    });
  }

  if (spO2ChartRef.value) {
    const ctx = spO2ChartRef.value.getContext('2d');
    spO2ChartInstance = new Chart(ctx, {
      type: 'line',
      data: createChartData('SpO2', 'SpO2', 'rgba(54, 162, 235, 1)'),
      options: createChartOptions(),
    });
  }

  if (BPMChartRef.value) {
    const ctx = BPMChartRef.value.getContext('2d');
    BPMChartInstance = new Chart(ctx, {
      type: 'line',
      data: createChartData('BPM', 'BPM', 'rgba(255, 206, 86, 1)'),
      options: createChartOptions(),
    });
  }

  if (gChartRef.value) {
    const ctx = gChartRef.value.getContext('2d');
    gChartInstance = new Chart(ctx, {
      type: 'line',
      data: createChartData('G-force', 'g', 'rgba(255, 99, 132, 1)', 'session-stats'),
      options: createChartOptions(),
    });
  }
};

// Watchers for Data and Refs
watch([concussionStats, sessionStats, selectedSessionId], initializeOrUpdateCharts, { immediate: true });

// Handle Canvas Ref Changes
watch([footingQualityChartRef, spO2ChartRef, BPMChartRef, gChartRef], ([newFootingRef, newSpO2Ref, newBPMRef, newGRef]) => {
  if (newFootingRef && newSpO2Ref && newBPMRef && newGRef) {
    initializeOrUpdateCharts();
  }
});
</script>


<template>
  <section>
    <div class="select-session">
      <h2>Sessions disponibles</h2>
      <select v-model="selectedSessionId">
        <option v-for="session in sessions" :key="session.session_id" :value="session.session_id">
          {{ session.session_name }} ({{ session.session_id }})
        </option>
      </select>
    </div>
    <div class="concussion-container">
      <div class="graphics-container">
        <div class="graph">
          <canvas ref="footingQualityChartRef"></canvas>
        </div>
        <div class="graph">
          <canvas ref="spO2ChartRef"></canvas>
        </div>
        <div class="graph">
          <canvas ref="gChartRef"></canvas>
        </div>
      </div>
      <div class="stats-container">
        <div class="stats">
            <div class="stats-item">
                <div class="stats-name">Footing Quality:</div>
                <div class="stats-data">
                    {{ latestConcussionStat && latestConcussionStat.footing_quality ? (latestConcussionStat.footing_quality * 100).toFixed(2) + '%' : 'N/A' }}
                </div>
            </div>
            <div class="stats-item">
                <div class="stats-name">Number of Shocks:</div>
                <div class="stats-data">
                    {{ latestConcussionStat?.number_of_shocks ?? 'N/A' }}
                </div>
            </div>
            <div class="stats-item">
                <div class="stats-name">Max G-force:</div>
                <div class="stats-data">
                    {{ latestConcussionStat && latestConcussionStat.max_g ? latestConcussionStat.max_g.toFixed(2) : 'N/A' }}
                </div>
            </div>
            <div class="stats-item">
                <div class="stats-name">BPM:</div>
                <div class="stats-data">
                    {{ latestConcussionStat && latestConcussionStat.BPM ? latestConcussionStat.BPM.toFixed(0) : 'N/A' }}
                </div>
            </div>
            <div class="stats-item">
                <div class="stats-name">SpO2:</div>
                <div class="stats-data">
                    {{ latestConcussionStat && latestConcussionStat.SpO2 ? latestConcussionStat.SpO2.toFixed(0) : 'N/A' }}
                </div>
            </div>
            <div class="stats-item">
                <div class="stats-name">Temperature:</div>
                <div class="stats-data">
                    {{ latestConcussionStat && latestConcussionStat.temperature ? latestConcussionStat.temperature.toFixed(1) + ' °C' : 'N/A' }}
                </div>
            </div>
        </div>

      </div>
    </div>
  </section>
</template>

