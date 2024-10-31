<script setup>

import { onMounted, ref } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const playerContainer = ref(null);

onMounted(() => {
    // Initialiser la scène, la caméra et le renderer
    const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth * 0.32 / window.innerHeight, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer({ antialias: true });

  // Définir la taille et ajouter le renderer dans le conteneur Vue
  renderer.setSize(window.innerWidth * 0.32, window.innerHeight);
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
    scene.add(gltf.scene);
  }, undefined, (error) => {
    console.error('An error happened', error);
  });

  // Positionner la caméra
  camera.position.z = 5;

  // Fonction d'animation
  function animate() {
    requestAnimationFrame(animate);

    // Mettre à jour les contrôles
    controls.update();

    // Rendre la scène
    renderer.render(scene, camera);
  }

  // Appel de la fonction d'animation
  animate();
});
</script>


<template>
    <section>
        <div ref="playerContainer" class="player-container"></div>
    </section>
</template>