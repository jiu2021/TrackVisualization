import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    name: 'test',
    path: '/test',
    component: () => import('@/components/Test.vue')
  },
  {
    name: 'login',
    path: '/login',
    component: () => import('@/components/Login.vue')
  },
  {
    name: 'home',
    path: '/home',
    component: () => import('@/components/Home/Home.vue')
  }
]


const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
