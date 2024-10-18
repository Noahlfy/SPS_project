// Load the data from the API
let sessionActive = false;
let sessionPaused = false;
document.getElementById("stop-button").disabled = true;

function updateButtonState(buttonId, borderColor, text = null, bgColor = null, textColor = null) {
    const button = document.getElementById(buttonId);
    if (text !== null) button.innerHTML = text;
    if (bgColor !== null) button.style.backgroundColor = bgColor;
    if (textColor !== null) button.style.color = textColor;
    button.style.borderColor = borderColor;
}

async function sendActionToBackend(action, sessionName = null) {
    let url;
    let method = 'POST';
    let body = {};

    switch(action) {
        case 'start':
            url = '/start_session';
            body = { session_name: sessionName };
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

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });
        return await response.json();
    } catch (error) {
        console.error('Error sending action to backend:', error);
    }
}

function startDataCollection() {
    if (typeof sessionPaused === 'undefined') {
        console.error('sessionPaused is not defined yet');
        return;
    }

    if (sessionPaused) {
        // Reprendre la session
        sessionPaused = false;
        document.getElementById("start-button").disabled = true;
        updateButtonState("start-button", "green", "Start");
        updateButtonState("stop-button", "red", "Pause");
        sendActionToBackend('start').then(data => {
            console.log('Session resumed:', data);
        });
    } else {
        // Démarrer une nouvelle session
        sessionActive = true;
        updateButtonState("stop-button", "red", "Pause");
        document.getElementById("stop-button").disabled = true;
        document.getElementById("start-button").disabled = true;

        // Demander le nom de la session
        const sessionInput = document.createElement("input");
        sessionInput.type = "text";
        sessionInput.id = "session-name";
        sessionInput.placeholder = "Session name";

        sessionInput.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();  
                const sessionName = sessionInput.value;

                console.log('Session Name:', sessionName);
                sendActionToBackend('start', sessionName).then(data => {
                    console.log('Session started with name:', sessionName);
                    sessionInput.remove();
                });
                document.getElementById("stop-button").disabled = false;
            }
        });

        const sessionContainer = document.getElementById('control-panel');
        sessionContainer.appendChild(sessionInput);
    }
}

function stopDataCollection() {
    if (sessionPaused) {
        // Arrêter la session
        sessionPaused = false;
        sessionActive = false;
        updateButtonState("start-button", "transparent", "Start");
        updateButtonState("stop-button", "transparent", "Stop");

        sendActionToBackend('exit').then(data => {
            console.log('Session stopped:', data);
        });
        document.getElementById("start-button").disabled = false;
        document.getElementById("stop-button").disabled = true;
    } else {
        // Mettre la session en pause
        sessionPaused = true;
        updateButtonState("start-button", "green", "Resume");
        updateButtonState("stop-button", "red", "Exit");

        sendActionToBackend('pause').then(data => {
            console.log('Session paused:', data);
        });
        document.getElementById("start-button").disabled = false;
    }
}
