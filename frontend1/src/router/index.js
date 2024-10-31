import { createRouter, createWebHistory } from 'vue-router'

import DashboardView from '@/views/DashboardView.vue';
import ConcussionView from '@/views/concussionView.vue';
import DatabaseView from '@/views/DatabaseView.vue';
import ParametersView from '@/views/ParametersView.vue';
import ActiveSessionView from '@/views/ActiveSessionView.vue';
import InactiveSessionView from '@/views/InactiveSessionView.vue';

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
      path: '/session/active',
      name: 'SessionActive',
      component: ActiveSessionView,
    },
    {
      path: '/session/inactive',
      name: 'SessionInactive',
      component: InactiveSessionView,
    },
    {
      path: '/parameters',
      name: 'Parameters',
      component: ParametersView,
    },
    
  ]
});

export default router
