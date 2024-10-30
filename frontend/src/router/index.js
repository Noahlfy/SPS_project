import { createRouter, createWebHistory } from 'vue-router'

import DashboardView from '@/views/DashboardView.vue';
import CommotionView from '@/views/CommotionView.vue';
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
    },
    {
      path: '/commotion',
      name: 'Commotion',
      component: CommotionView,
    },
    {
      path: '/database',
      name: 'Database',
      component: DatabaseView,
    },
    {
      path: '/session',
      name: 'Session',
      component: SessionView,
    },
    {
      path: '/parameters',
      name: 'Parameters',
      component: ParametersView,
    },
  ]
});

export default router
