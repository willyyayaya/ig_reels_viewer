import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import HistoryView from '../views/HistoryView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        title: '觀看任務'
      }
    },
    {
      path: '/history',
      name: 'history',
      component: HistoryView,
      meta: {
        title: '歷史記錄'
      }
    }
  ]
})

// 設置頁面標題
router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} - Instagram Reels Viewer` : 'Instagram Reels Viewer'
})

export default router
