import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import TaskMonitor from '@/views/TaskMonitor.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/monitor',
      name: 'TaskMonitor',
      component: TaskMonitor
    }
  ]
})

export default router
