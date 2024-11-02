// src/services/apiService.js

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
