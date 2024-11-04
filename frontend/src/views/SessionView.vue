<script setup>


import Navbar from '@/components/Navbar.vue';
import SearchBar from '@/components/SearchBar.vue';
import SessionGraphs from '@/components/SessionGraphs.vue';
import SessionStats from '../components/SessionStats.vue';

import { ref, computed } from 'vue';
import { useDataStore } from '@/stores/dataStore';

const dataStore = useDataStore();

const sessions = computed(() => dataStore.session || []);
const selectedSessionId = ref(dataStore.selectedSessionId);

const onSessionChange = () => {
  dataStore.selectSession(selectedSessionId.value);
};


</script>

<template>
    <Navbar />   
    <SearchBar />   
    <div class="select-session">
        <h2>Sessions disponibles</h2>
        <select v-model="selectedSessionId" @change="onSessionChange">
        <option v-for="session in sessions" :key="session.session_id" :value="session.session_id">
            {{ session.session_name }} ({{ session.session_id }})
        </option>
        </select>
    </div>
    <SessionGraphs />
    <SessionStats />
</template>
