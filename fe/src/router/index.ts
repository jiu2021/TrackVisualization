import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/test'
  },
  {
    path: '/test',
    component: () => import('@/components/Test.vue')
  },
  {
    path: '/login',
    component: () => import('@/components/Login.vue')
  },
  {
    path: '/home',
    component: () => import('@/components/Home/Home.vue')
  }
]


const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
