import './assets/main.css';
import 'primeicons/primeicons.css';
import router from './router';

// main.js
import { createApp } from 'vue';
import App from './App.vue';
import pinia from './pinia'; // Importez l'instance de Pinia

const app = createApp(App);

app.use(pinia); // Utilisez l'instance de Pinia avec votre application
app.use(router)
app.mount('#app');

