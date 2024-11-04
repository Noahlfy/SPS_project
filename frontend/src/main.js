import './assets/main.css';
import 'primeicons/primeicons.css';
import router from './router';

// main.js
import { createApp } from 'vue';
import App from './App.vue';
import pinia from './pinia'; // Importez l'instance de Pinia

// Importation de Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

// Ajout d'icônes spécifiques
import { faHome, faDatabase, faRunning, faExclamationTriangle, faCog, faStopwatch } from '@fortawesome/free-solid-svg-icons';
library.add(faHome, faDatabase, faRunning, faExclamationTriangle, faCog, faStopwatch); 


const app = createApp(App);

app.component('font-awesome-icon', FontAwesomeIcon);

app.use(pinia); // Utilisez l'instance de Pinia avec votre application
app.use(router)
app.mount('#app');

