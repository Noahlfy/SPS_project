import { createRouter, createWebHistory } from 'vue-router'

import DashboardView from '@/views/DashboardView.vue';
import ConcussionView from '@/views/ConcussionView.vue';
import DatabaseView from '@/views/DatabaseView.vue';
import ParametersView from '@/views/ParametersView.vue';
import SessionView from '@/views/SessionView.vue';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: DashboardView,
      meta: { keepAlive: true } 
    },
    {
      path: '/concussion',
      name: 'Concussion',
      component: ConcussionView,
      meta: { keepAlive: true } 
    },
    {
      path: '/database',
      name: 'Database',
      component: DatabaseView,
      meta: { keepAlive: true } 
    },
    {
      path: '/session',
      name: 'Session',
      component: SessionView,
      meta: { keepAlive: true } 
    },

    {
      path: '/parameters',
      name: 'Parameters',
      component: ParametersView,
      meta: { keepAlive: true } 
    },
    
  ]
});

export default router
