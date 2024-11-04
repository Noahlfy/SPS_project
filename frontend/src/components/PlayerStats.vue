<script setup>
import { onMounted, ref } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const playerContainer = ref(null);

onMounted(() => {
    // Initialiser la scène, la caméra et le renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth * 0.27 / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

    // Définir la taille et ajouter le renderer dans le conteneur Vue
    const containerWidth = playerContainer.value.clientWidth;
    const containerHeight = playerContainer.value.clientHeight;
    renderer.setSize(containerWidth, containerHeight);
    playerContainer.value.appendChild(renderer.domElement);

    // Initialiser les contrôles d'orbite
    const controls = new OrbitControls(camera, renderer.domElement);
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
    pointLight.position.set(50, 50, 50);
    scene.add(pointLight);

    // Charger le modèle GLTF
    const loader = new GLTFLoader();
    const modelPath = new URL('../assets/character.glb', import.meta.url).href;

    loader.load(modelPath, (gltf) => {
        const model = gltf.scene;
        model.position.set(0, -1.25, 0); // Ajuster la position pour mieux centrer le modèle
        model.scale.set(1.75, 1.75, 1.75); // Ajuster la taille du modèle si nécessaire
        scene.add(model);
    }, undefined, (error) => {
        console.error('An error happened', error);
    });

    // Positionner la caméra
    camera.position.set(0, 1.5, 5);

    // Fonction d'animation
    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }

    // Appel de la fonction d'animation
    animate();

    // Adapter la taille du renderer lors du redimensionnement de la fenêtre
    window.addEventListener('resize', () => {
        const newWidth = playerContainer.value.clientWidth;
        const newHeight = playerContainer.value.clientHeight;
        camera.aspect = newWidth / newHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(newWidth, newHeight);
    });
});
</script>




<template>
    <section>
        <div ref="playerContainer" class="session-player-container"></div>
    </section>
</template>