import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/test'
  },
  {
    path: '/test',
    component: () => import('../src/components/Test.vue')
  }
]


const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
