<!-- App.vue -->
<script setup>
import { onMounted, onBeforeUnmount } from 'vue';
import { initializeData, initializeWebSocket, closeWebSocket } from "@/services/apiServices";

onMounted(() => {
  initializeData();
  initializeWebSocket();
});

onBeforeUnmount(() => {
  closeWebSocket();
});

</script>

<template>
  <router-view />
</template>
