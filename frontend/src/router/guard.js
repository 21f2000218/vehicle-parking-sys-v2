import store from '@/store';

export function requireAuth(to, _, next) {
  if (!store.getters['auth/isAuthenticated']) {
    return next('/login');
  }
  next();
}

export function requireAdmin(to, _, next) {
  if (!store.getters['auth/isAuthenticated']) {
    return next('/login');
  }
  if (!store.getters['auth/getUser'].role === 'admin') {
    return next('/user/dashboard');
  }
  next();
}

export function requireUser(to, _, next) {
  if (!store.getters['auth/isAuthenticated']) {
    return next('/login');
  }
  if (store.getters['auth/getUser'].role !== 'user') {
    return next('/admin/dashboard');
  }
  next();
}
