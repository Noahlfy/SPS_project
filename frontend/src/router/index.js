import { createRouter, createWebHistory } from 'vue-router'

import DashboardView from '@/views/DashboardView.vue';
import ConcussionView from '@/views/concussionView.vue';
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
      path: '/concussion',
      name: 'Concussion',
      component: ConcussionView,
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
