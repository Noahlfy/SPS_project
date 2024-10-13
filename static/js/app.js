// Load the data from the API

let sessionActive = false;
let sessionPaused = false;

function updateButtonState(buttonId, text, bgColor, textColor, borderColor) {
    const button = document.getElementById(buttonId);
    button.innerHTML = text;
    button.style.backgroundColor = bgColor;
    button.style.color = textColor;
    button.style.borderColor = borderColor;
}

function sendActionToBackend(action, sessionName = null) {
    let url;
    let method = 'POST';
    let body = {};

    switch(action) {
        case 'start':
            url = '/start_session';
            body = { session_name: sessionName };  // Envoi du nom de la session si défini
            break;
        case 'pause':
            url = '/pause_session';
            break;
        case 'exit':
            url = '/stop_session';
            break;
        default:
            console.error('Unknown action:', action);
            return Promise.reject('Unknown action');
    }
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    })
    .then(response => response.json())
    .catch(error => console.error('Error sending action to backend:', error));
}


function startDataCollection() {
    if (sessionPaused) {
        // Reprendre la session (après une pause)
        sessionPaused = false;
        updateButtonState("start-button", "Start", "green", "white", "green");
        updateButtonState("stop-button", "Stop", "red", "white", "red");
        document.getElementById("start-button").disabled = true;

        // Envoyer l'action "pause" au back-end
        sendActionToBackend('start')
        .then(data => {
            console.log('Session resumed:', data);
        });
    } else {
        // Démarrer une nouvelle session
        sessionActive = true;
        updateButtonState("stop-button", "Pause", "red", "white", "red");

        // Demander le nom de la session
        const sessionInput = document.createElement("input");
        sessionInput.type = "text";
        sessionInput.id = "session-name";
        sessionInput.placeholder = "Session name";

        sessionInput.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();  // Empêche le comportement par défaut
                const sessionName = sessionInput.value;

                // Log et soumission de la session
                console.log('Session Name:', sessionName);
                sendActionToBackend('start', sessionName).then(data => {
                    console.log('Session started with name:', sessionName);
                    sessionInput.remove();  // Retirer le champ de texte après soumission
                });
            }
        });

        // Ajouter l'élément à une partie spécifique de la page
        const sessionContainer = document.getElementById('session-container');
        sessionContainer.appendChild(sessionInput);
    }

    document.getElementById("start-button").disabled = true;
}

function stopDataCollection() {
    if (sessionPaused) {
        // Arrêter la session
        sessionActive = false;
        updateButtonState("start-button", "Start", "green", "white", "green");
        updateButtonState("stop-button", "Stop", "red", "white", "red");

        sendActionToBackend('exit').then(data => {
            console.log('Session stopped:', data);
        });
        document.getElementById("start-button").disabled = true;
    } else {
        // Mettre la session en pause
        sessionPaused = true;
        updateButtonState("start-button", "Resume", "green", "white", "green");
        updateButtonState("stop-button", "Exit", "red", "white", "red");

        sendActionToBackend('pause').then(data => {
            console.log('Session paused:', data);
        });
        document.getElementById("start-button").disabled = false;
    }
}



// Manage the database
const sensorColumns = {
    "BNO055_head": ["Session ID", "Time", "Accel X", "Accel Y", "Accel Z", "Quat W", "Quat X", "Quat Y", "Quat Z"],
    "BNO055_chest": ["Session ID", "Time", "Accel X", "Accel Y", "Accel Z", "Quat W", "Quat X", "Quat Y", "Quat Z"],
    "BNO055_right_leg": ["Session ID", "Time", "Accel X", "Accel Y", "Accel Z", "Quat W", "Quat X", "Quat Y", "Quat Z"],
    "BNO055_left_leg": ["Session ID", "Time", "Accel X", "Accel Y", "Accel Z", "Quat W", "Quat X", "Quat Y", "Quat Z"],
    "MAX30102": ["Session ID", "Time", "SpO2", "BPM"],
    "BMP280": ["Session ID", "Time", "Temperature", "Pressure", "Altitude"]
};


function updateTableColumns() {
    const sensorSelect = document.getElementById("sensor-select");
    const selectedSensor = sensorSelect.value;

    const tableHeader = document.getElementById("table-header");
    tableHeader.innerHTML = ""; // Efface l'en-tête existant

    const columns = sensorColumns[selectedSensor]

    columns.forEach(column => {
        const th = document.createElement("th");
        th.innerText = column;
        tableHeader.appendChild(th);
    });


    // Appel à l'API pour récupérer les données
    fetch(`/api/data?sensor=${selectedSensor}`)
        .then(response => response.json())
        .then(data => {
            // Appel de la fonction pour afficher les données ou des lignes vides
            updateTableData(data, columns);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Si une erreur se produit, on affiche quand même des lignes vides
            updateTableData([], columns);
        });
}

// Appel initial pour configurer le tableau avec le premier capteur par défaut
window.onload = updateTableColumns;

// Fonction pour afficher les données ou des lignes vides
function updateTableData(data, columns) {
    const dataBody = document.getElementById('dataBody');
    dataBody.innerHTML = '';  // Vider le tableau avant de l'actualiser

    if (data.lenght > 0) {
        data.forEach(row => {
            const newRow = document.createElement('tr');

            columns.forEach(column => {
                const td = document.createElement('td');
                td.innerText = row[column];
                newRow.appendChild(td);
            });
            data.appendChild(newRow);
        })
    }

    const rowToFill = 25 - data.length;
    for (let i = 0; i < rowToFill; i++) {
        const newRow = document.createElement('tr');
        columns.forEach(() => {
            const td = document.createElement('td');
            td.innerText = '';
            newRow.appendChild(td);
        });
        dataBody.appendChild(newRow);
    }
}




