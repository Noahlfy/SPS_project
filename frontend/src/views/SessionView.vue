<script setup>
import Navbar from '@/components/Navbar.vue';
import SearchBar from '@/components/SearchBar.vue';
import Graphs from '@/components/Graphs.vue';
import SessionStats from '../components/SessionStats.vue';
</script>

<template>
<Navbar />   
<SearchBar />   
<Graphs />
<session-stats />
</template>