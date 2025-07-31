import LoginPage from '@/views/LoginPage.vue';
import SignupPage from '@/views/SignupPage.vue';
import UserDashboard from '@/views/user/UserDashboard.vue';
import UserSearch from '@/views/user/UserSearch.vue';
import { createRouter, createWebHistory } from 'vue-router';

import AdminDashboard from '@/views/admin/AdminDashboard.vue';
import AdminManagement from '@/views/admin/AdminManagement.vue';
import AdminSearch from '@/views/admin/AdminSearch.vue';
import AdminUsers from '@/views/admin/AdminUsers.vue';
import { requireAdmin, requireUser } from './guard';
import UserSummary from '@/views/user/UserSummary.vue';
import AdminSummary from '@/views/admin/AdminSummary.vue';

const routes = [
  { path: '/login', component: LoginPage },
  { path: '/signup', component: SignupPage },
  { path: '/', redirect: '/login' },
  { path: '/user/dashboard', component: UserDashboard, beforeEnter: requireUser },
  { path: '/user/search', component: UserSearch, beforeEnter: requireUser },
  { path: '/user/summary', component: UserSummary, beforeEnter: requireUser },
  { path: '/admin/dashboard', component: AdminDashboard, beforeEnter: requireAdmin },
  { path: '/admin/management', component: AdminManagement, beforeEnter: requireAdmin },
  { path: '/admin/search', component: AdminSearch, beforeEnter: requireAdmin },
  { path: '/admin/users', component: AdminUsers, beforeEnter: requireAdmin },
  { path: '/admin/summary', component: AdminSummary, beforeEnter: requireAdmin },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;