<script setup>
import {RouterLink} from 'vue-router'
</script>

<template>
    <nav class="bg-green-700 border-b border-green-500 h-screen flex flex-col items-center justify-start py-4 space-y-6">
        <RouterLink to="/" class="text-green-300 hover:text-green-400">
            <i class="pi pi-home text-4xl"></i>
        </RouterLink>

        <RouterLink to="/database" class="text-green-300 hover:text-green-400">
            <i class="pi pi-database text-4xl"></i>
        </RouterLink>

        <RouterLink to="/session" class="text-green-300 hover:text-green-400">
            <i class="fas fa-running text-4xl"></i>
        </RouterLink>

        <RouterLink to="/commotion" class="text-green-300 hover:text-green-400">
            <i class="pi pi-exclamation-triangle text-4xl"></i>
        </RouterLink>

        <RouterLink to="/parameters" class="text-green-300 hover:text-green-400">
            <i class="pi pi-cog text-4xl"></i>
        </RouterLink>
    </nav>

</template>