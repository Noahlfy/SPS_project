// src/eventBus.js
import { reactive } from 'vue';

export const eventBus = reactive({
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
    'temperature': [],
    'concussion-stats': [],
    'session-stats': [],
    'dashboard-stats': [],
});
