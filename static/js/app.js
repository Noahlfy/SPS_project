// search bar

const searchIcon = document.getElementById('searchIcon');
const searchInput = document.getElementById('searchInput')

searchIcon.addEventListener('click', function() {
    searchInput.focus(); 
});

// Load the data from the API

let sessionActive = false;
let sessionPaused = false;
document.getElementById("stop-button").disabled = true;
document.getElementById("stop-button").disabled = true;

function updateButtonState(buttonId, borderColor, text = null, bgColor = null, textColor = null) {
function updateButtonState(buttonId, borderColor, text = null, bgColor = null, textColor = null) {
    const button = document.getElementById(buttonId);
    if (text !== null) button.innerHTML = text;
    if (bgColor !== null) button.style.backgroundColor = bgColor;
    if (textColor !== null) button.style.color = textColor;
    if (text !== null) button.innerHTML = text;
    if (bgColor !== null) button.style.backgroundColor = bgColor;
    if (textColor !== null) button.style.color = textColor;
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
    document.getElementById("start-button").disabled = true;
    document.getElementById("start-button").disabled = true;
    if (sessionPaused) {
        // Reprendre la session (après une pause)
        sessionPaused = false;
        updateButtonState("start-button","green", "Start");
        updateButtonState("stop-button", "red", "Stop")
        updateButtonState("start-button","green", "Start");
        updateButtonState("stop-button", "red", "Stop")
        // Envoyer l'action "pause" au back-end
        sendActionToBackend('start')
        .then(data => {
            console.log('Session resumed:', data);
        });
    } else {
        // Démarrer une nouvelle session
        sessionActive = true;
        updateButtonState("stop-button", "red", "Pause");
        document.getElementById("stop-button").disabled = true;
        updateButtonState("stop-button", "red", "Pause");
        document.getElementById("stop-button").disabled = true;
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
                document.getElementById("stop-button").disabled = false;
                document.getElementById("stop-button").disabled = false;
            }
        });

        // Ajouter l'élément à une partie spécifique de la page
        const sessionContainer = document.getElementById('session-container');
        sessionContainer.appendChild(sessionInput);
    }
}

function stopDataCollection() {
    if (sessionPaused) {
        // Arrêter la session
        sessionPaused = false;
        sessionPaused = false;
        sessionActive = false;
        updateButtonState("start-button", "transparent", "Start");
        updateButtonState("stop-button", "transparent", "Stop");
        updateButtonState("start-button", "transparent", "Start");
        updateButtonState("stop-button", "transparent", "Stop");

        sendActionToBackend('exit').then(data => {
            console.log('Session stopped:', data);
        });
        document.getElementById("start-button").disabled = false;
        document.getElementById("stop-button").disabled = true;

        document.getElementById("start-button").disabled = false;
        document.getElementById("stop-button").disabled = true;

    } else {
        // Mettre la session en pause
        sessionPaused = true;
        updateButtonState("start-button", "green", "Resume");
        updateButtonState("stop-button", "red", "Exit");
        updateButtonState("start-button", "green", "Resume");
        updateButtonState("stop-button", "red", "Exit");

        sendActionToBackend('pause').then(data => {
            console.log('Session paused:', data);
        });
        document.getElementById("start-button").disabled = false;
    }
}



// Initialiser la scène, la caméra et le renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth * 0.3 / window.innerHeight, 0.1, 1000); // Ajuster le rapport d'aspect
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth * 0.27, window.innerHeight); // Ajuste la taille du renderer pour correspondre au conteneur fixe
renderer.setClearColor(0x000000, 0); // Définir la couleur de fond en transparent
document.querySelector('.fixed-container').appendChild(renderer.domElement);

// Ajouter des contrôles d'orbite
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; // Activer l'amortissement (inertie)
controls.dampingFactor = 0.25; // Facteur d'amortissement
controls.enableZoom = true; // Activer le zoom

// Ajouter des lumières supplémentaires
const ambientLight = new THREE.AmbientLight(0x404040, 10); 
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(0, 1, 1).normalize();
scene.add(directionalLight);

const pointLight = new THREE.PointLight(0xffffff, 1, 100);
pointLight.position.set(5, 5, 5);
scene.add(pointLight);

// Charger le modèle GLTF
const loader = new THREE.GLTFLoader();
loader.load('../Animation/character.glb', function(gltf) {
    const humanModel = gltf.scene;
    scene.add(humanModel);


    
    // Ajuster l'échelle du modèle
    humanModel.scale.set(1.9, 1.9, 1.9); // Agrandir le modèle (x1.5 dans chaque dimension)

    // Ajuster la position du modèle
    humanModel.position.y = -2.5; // Déplacer le modèle vers le bas

    // Positionner la caméra
    camera.position.z = 5;
    camera.position.y = 1; // Ajuster la position de la caméra pour mieux aligner le modèle

    // Fonction d'animation
    function animate() {
        requestAnimationFrame(animate);
        controls.update(); // Mettre à jour les contrôles
        renderer.render(scene, camera);
    }
    animate();
}, undefined, function(error) {
    console.error('Error loading the model:', error);
});



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
