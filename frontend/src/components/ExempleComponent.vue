<!-- ExempleComponent.vue -->
<script setup>
import { computed } from 'vue';
import { useDataStore } from '@/stores/dataStore';

const dataStore = useDataStore();

const headData = computed(() => dataStore.head);
</script>

<template>
  <div>
    <h1>Données du capteur Head</h1>
    <ul>
      <li v-for="item in headData" :key="item.id">
        {{ item }}
      </li>
    </ul>
  </div>
</template>
