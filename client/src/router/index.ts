import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes: RouteConfig[] = [
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: '/lamps',
    name: 'lamps',
    component: () => import('../views/Lamps.vue'),
  },
  {
    path: '/lamps/:id/settings',
    name: 'lamp-settings',
    component: () => import('../views/LampSettings.vue'),
  },
  {
    path: '/group/:id',
    name: 'group',
    component: () => import('../views/Group.vue'),
  },
  {
    path: '/setup',
    name: 'setup',
    component: () => import('../views/Setup.vue'),
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
})

export default router
