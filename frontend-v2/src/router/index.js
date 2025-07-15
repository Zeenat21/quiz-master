// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminDash from '../views/Admin/AdminDash.vue'
import UserDash from '@/views/User/UserDash.vue'
import Home from '@/views/Home.vue'
import PublicLayout from '@/components/PublicLayout.vue';
import About from '@/views/About.vue'
const routes = [

  // Public routes
  {
    path: '/',
    component: PublicLayout,
    children: [
      { path: '', component: Home },
      { path: 'about', component: About },
    ]
  },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  
  {
  path: '/admin',
  component: AdminDash,
  meta: { requiresAuth: true, role: 'admin' },
  children: [
    { path: '', component: () => import('@/views/Admin/AdminHome.vue') },
    { path: 'subjects', component: () => import('@/views/Admin/Subjects.vue') },
    { path: 'users', component: () => import('@/views/Admin/Users.vue') },
    { path: 'quizzes', component: () => import('@/views/Admin/Quizzes.vue') },
    { path: 'search', component: () => import('@/views/Admin/Search.vue') },
    { path: 'summary', component: () => import('@/views/Admin/Summary.vue') },
  ]
}, 
{
  path: '/user',
  component: UserDash,
  meta: { requiresAuth: true, role: 'user' },
  children: [
    { path: '', component: () => import('@/views/User/UserHome.vue') },
    { path: 'scores', component: () => import('@/views/User/Scores.vue') },
    { path: 'profile', component: () => import('@/views/User/Profile.vue') },
    { path: 'summary', component: () => import('@/views/User/Summary.vue') },
    { path: 'quiz-attempt/:quizId', component: () => import('@/views/User/QuizAttempt.vue'),}
  ]
}


]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiredRole = to.meta.role;

  const token = localStorage.getItem('access_token');
  const roles = JSON.parse(localStorage.getItem('user_roles') || '[]');

  if (requiresAuth) {
    if (!token) {
      next('/login');
    } else if (requiredRole && !roles.includes(requiredRole)) {
      next('/login');
    } else {
      next();
    }
  } else {
    next();
  }
});


export default router

