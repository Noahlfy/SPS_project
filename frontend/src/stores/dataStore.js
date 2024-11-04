// src/stores/dataStore.js
import { defineStore } from 'pinia';

export const useDataStore = defineStore('data', {
  state: () => ({
    session: [],
    head: [],
    'head-transformed': [],
    chest: [],
    'chest-transformed': [],
    'right-leg': [],
    'right-leg-transformed': [],
    'left-leg': [],
    'left-leg-transformed': [],
    'heart-rate': [],
    temperature: [],
    'concussion-stats': [],
    'session-stats': [],
    'dashboard-stats': [],
  }),
  actions: {
    updateData(key, data) {
      this.$patch({
        [key]: data ? [...data] : [],
      });
    },
    selectSession(sessionId) {
        this.selectedSessionId = sessionId;
    },
  },
});
