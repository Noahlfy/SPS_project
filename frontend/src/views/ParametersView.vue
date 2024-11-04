<script setup>
import Navbar from '@/components/Navbar.vue';
import SearchBar from '@/components/SearchBar.vue';

</script>

<template>
    <Navbar />
    <SearchBar />

    <section>
        
  
        <h2>Player Profile Settings</h2>
        <form>
        <label for="playerName">Player Name:</label>
        <input type="text" id="playerName" placeholder="John Doe" />

        <label for="age">Age:</label>
        <input type="number" id="age" placeholder="25" />

        <label for="height">Height (cm):</label>
        <input type="number" id="height" placeholder="180" />

        <label for="weight">Weight (kg):</label>
        <input type="number" id="weight" placeholder="85" />



        <button type="submit">Save Profile</button>
        </form>
  </section>
</template>

<style scoped>
/* Add basic styling */
section {
    position: fixed;
    max-width: 35%;
    margin-top: 14%;
    margin-left: 45%;
}

label {
  display: block;
  margin-top: 10px;
  font-weight: bold;
}

input, select, button {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  box-sizing: border-box;
}
</style>


