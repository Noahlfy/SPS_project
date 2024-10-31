
// Start a session
const start_button = document.getElementById('startButton');
start_button.addEventListener('click', function() {
    window.location.href = 'session.html'; 
});


// Update data

function updateDashboard() {
    fetch('/api/data/dashboard') 
    .then(response => response.json())
    .then(data => {
        const last_session_state = data.dashboard.last_session_state;
        const last_session_risk = data.dashboard.last_session_risk;
        const concussion_passport = data.dashboard.concussion_passport;
        const average_activity_during_sessions = data.dashboard.average_activity_during_sessions;
        const average_heart_rate = data.dashboard.average_heart_rate;

        document.getElementById('last_session_state').innertext = last_session_state; 
        document.getElementById('last-session-risk').innertext = last_session_risk;
        document.getElementById('concussion_passport').innertext = concussion_passport;
        document.getElementById('average_activity_during_sessions').innertext = average_activity_during_sessions;
        document.getElementById('average_heart_rate').innertext = average_heart_rate;
    })
}



// Initialiser la scène, la caméra et le renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth * 0.3 / window.innerHeight, 0.1, 1000); // Ajuster le rapport d'aspect
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth*0.32, window.innerHeight); // Ajuste la taille du renderer pour correspondre au conteneur fixe
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
loader.load('static/Animation/character.glb', function(gltf) {
    const humanModel = gltf.scene;
    scene.add(humanModel);

    // Ajuster l'échelle du modèle
    humanModel.scale.set(1.75, 1.75, 1.75); // Agrandir le modèle (x1.5 dans chaque dimension)

    // Ajuster la position du modèle
    humanModel.position.y = -1.35; // Déplacer le modèle vers le bas

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
