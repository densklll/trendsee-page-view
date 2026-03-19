import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'search',
      component: () => import('../views/SearchResultsView.vue'),
    },
    {
      path: '/video/:id',
      name: 'video-detail',
      component: () => import('../views/VideoDetailView.vue'),
    },
  ],
})

export default router
