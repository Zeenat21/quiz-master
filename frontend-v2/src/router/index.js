// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminDash from '../views/Admin/AdminDash.vue'
import UserDash from '@/views/User/UserDash.vue'

const routes = [

  { path: '/login', component: Login },
  { path: '/register', component: Register },
  
  {
  path: '/admin',
  component: AdminDash,
  children: [
    { path: '', component: () => import('@/views/Admin/AdminHome.vue') },
    { path: 'subjects', component: () => import('@/views/Admin/Subjects.vue') },
    { path: 'users', component: () => import('@/views/Admin/Users.vue') },
    { path: 'quizzes', component: () => import('@/views/Admin/Quizzes.vue') },
    // { path: 'questions', component: () => import('@/views/Questions.vue') },
    { path: 'search', component: () => import('@/views/Admin/Search.vue') },
    { path: 'summary', component: () => import('@/views/Admin/Summary.vue') },
  ]
}, 
{
  path: '/user',
  component: UserDash,
  children: [
    { path: '', component: () => import('@/views/User/UserHome.vue') },
    { path: 'scores', component: () => import('@/views/User/Scores.vue') },
    { path: 'profile', component: () => import('@/views/User/Profile.vue') },
     { path: 'summary', component: () => import('@/views/User/Summary.vue') },
    // { path: 'quizzes', component: () => import('@/views/Admin/Quizzes.vue') },
    // { path: 'questions', component: () => import('@/views/Questions.vue') },
    // { path: 'search', component: () => import('@/views/Admin/Search.vue') },
   
  ]
}


]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router


