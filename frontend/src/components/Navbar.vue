<script setup>
import {RouterLink, useRoute} from 'vue-router'

const isActiveLink = (routePath) => {
    const route = useRoute();
    return route.path === routePath;
}
</script>

<template>
    <nav>
        <div class="nav-icon">
            <RouterLink to="/" 
            :class="[isActiveLink('/')
            ? 'text-primary'
            : 'text-white',
            'hover:text-secondary'
            ]">
                <i class="pi pi-home text-5xl"></i>
            </RouterLink>
        </div>
        <div class="nav-icon">
            <RouterLink to="/database" 
            :class="[isActiveLink('/database')
            ? 'text-primary'
            : 'text-white',
            'hover:text-secondary'
            ]">
                <i class="pi pi-database text-5xl"></i>
            </RouterLink>
        </div>
        <div class="nav-icon">
            <RouterLink to="/session" 
            :class="[isActiveLink('/session')
            ? 'text-primary'
            : 'text-white',
            'hover:text-secondary'
            ]">
                <i class="fas fa-running text-5xl"></i>
            </RouterLink>
        </div>
        <div class="nav-icon">
            <RouterLink to="/concussion" 
            :class="[isActiveLink('/concussion')
            ? 'text-primary'
            : 'text-white',
            'hover:text-secondary'
            ]">
                <i class="pi pi-exclamation-triangle text-5xl"></i>
            </RouterLink>
        </div>
        <div class="nav-icon">
            <RouterLink to="/parameters" 
            :class="[isActiveLink('/parameters')
            ? 'text-primary'
            : 'text-white',
            'hover:text-secondary'
            ]">
                <i class="pi pi-cog text-5xl"></i>
            </RouterLink>
        </div>
    </nav>

</template>