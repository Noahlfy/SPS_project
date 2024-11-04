// src/services/apiServices.js
import { useDataStore } from '@/stores/dataStore';
import pinia from '@/pinia';
import { setActivePinia } from 'pinia';

setActivePinia(pinia); // Définit l'instance active de Pinia

const dataStore = useDataStore(pinia);

// src/services/apiServices.js

// Mapping des clés des données reçues vers les clés du store Pinia
const keyMap = {
    session_data: 'session',
    head_data: 'head',
    head_transformed_data: 'head-transformed',
    chest_data: 'chest',
    chest_transformed_data: 'chest-transformed',
    right_leg_data: 'right-leg',
    right_leg_transformed_data: 'right-leg-transformed',
    left_leg_data: 'left-leg',
    left_leg_transformed_data: 'left-leg-transformed',
    heart_rate_data: 'heart-rate',
    temperature_data: 'temperature',
    concussion_stats_data: 'concussion-stats',
    session_stats_data: 'session-stats',
    dashboard_stats_data: 'dashboard-stats',
  };
  

export function initializeDataStore() {
    dataStore = useDataStore(pinia); // Initialisez le store ici
  }

export const getSessionId = async () => {
    try {
        const response = await fetch('http://localhost:8000/api/session/');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        let last_session_id = 0
        data.forEach((session) => {
            if (session.session_id > last_session_id) {
                last_session_id = session.session_id;
            };
        })
        return last_session_id;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error; // Relance l'erreur pour la gestion ultérieure
    }
};


// Fonction pour initialiser les données
export const initializeData = () => {
    if (!dataStore) {
      console.error('Data store is not initialized.');
      return;
    }
    
    const keys = Object.keys(dataStore.$state);
    keys.forEach(key => {
      fetch(`http://localhost:8000/api/${key}/`)
        .then(response => response.json())
        .then(data => {
          dataStore.updateData(key, data);
        })
        .catch(error => {
          console.error(`Error fetching data for ${key}:`, error);
          dataStore.updateData(key, []);
        });
    });
    console.log("Fin de l'initialisation des données");
  };
  
  // WebSocket en direct
  let socket;
  let isConnected = false;
  
  export function initializeWebSocket() {
    if (!isConnected) {  // Assure que le WebSocket n'est initialisé qu'une seule fois
      socket = new WebSocket("ws://localhost:8000/ws/data/");
      isConnected = true;
  
      socket.onopen = () => {
        console.log("Connexion WebSocket établie.");
      };
  
      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("Données reçues via WebSocket :", data);
        handleWebSocketData(data);
      };
  
      socket.onerror = (error) => {
        console.error("Erreur WebSocket :", error);
        isConnected = false;  // Réinitialise la connexion en cas d'erreur
      };
  
      socket.onclose = () => {
        console.log("Connexion WebSocket fermée.");
        isConnected = false;  // Permet de réinitialiser la connexion si besoin
      };
    }
  }
  
  // Fonction pour gérer les données reçues via WebSocket
// Fonction pour gérer les données reçues via WebSocket
function handleWebSocketData(data) {
    if (data && dataStore) {
      Object.keys(data).forEach(key => {
        const storeKey = keyMap[key]; // Obtenir la clé correspondante dans le store
        if (storeKey && storeKey in dataStore.$state) {
          dataStore.updateData(storeKey, data[key]);
        } else {
          console.warn(`La clé ${key} n'a pas de correspondance dans le store.`);
        }
      });
    }
  }
  
  
  
  export function closeWebSocket() {
    if (socket) {
      socket.close();
      isConnected = false;
    }
  }