<script setup>
import Navbar from '@/components/Navbar.vue';
import SearchBar from '@/components/SearchBar.vue';
import Player from '@/components/Player.vue';
import DashboardContainer from '@/components/DashboardContainer.vue';
import { getSessionId } from '@/services/apiServices';
</script>

<template>
	<SearchBar />   
	<Navbar />   
	<Player />
	<DashboardContainer />
</template>