import { authService } from '@/api/authService';
import { jwtDecode } from 'jwt-decode';

const STORAGE_KEY = 'auth';

export default {
  namespaced: true,
  state: () => {
    const saved = JSON.parse(sessionStorage.getItem(STORAGE_KEY));
    return saved || {
      accessToken: null,
      refreshToken: null,
      user: null
    };
  },
  mutations: {
    SET_TOKENS(state, { accessToken, refreshToken }) {
      state.accessToken = accessToken;
      state.refreshToken = refreshToken;
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    },
    SET_USER(state, user) {
      console.log(user)
      console.log(state)
      state.user = user;
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    },
    CLEAR_AUTH(state) {
      state.accessToken = null;
      state.refreshToken = null;
      state.user = null;
      sessionStorage.removeItem(STORAGE_KEY);
    }
  },
  actions: {
    async login({ commit }, { username, password }) {
      const res = await authService.login({ username, password });
      console.log("Login")
      console.log(res)
      const { access_token, refresh_token } = res;

      const decoded = jwtDecode(access_token);
      const user = {
        username: username,
        id: decoded.sub,
        role: decoded.role,
        exp: decoded.exp
      };

      commit('SET_TOKENS', {
        accessToken: access_token,
        refreshToken: refresh_token
      });
      commit('SET_USER', user);
    },

    async register({ dispatch }, data) {
      await authService.register(data);
      await dispatch('login', {
        username: data.username,
        password: data.password
      });
    },

    async refreshToken({ state, commit }) {
      const res = await authService.refresh(state.refreshToken);
      const access_token = res.data.access_token;
      const decoded = jwtDecode(access_token);
      const user = {
        id: decoded.sub,
        role: decoded.role,
        exp: decoded.exp
      };
      commit('SET_TOKENS', {
        accessToken: access_token,
        refreshToken: state.refreshToken
      });
      commit('SET_USER', user);
      return access_token;
    },

    async logout({ commit }) {
      try { await authService.logout(); } catch (_) { }
      commit('CLEAR_AUTH');
    }
  },
  getters: {
    isAuthenticated: state => !!state.accessToken,
    getUser: state => state.user,
    isAdmin: state => state.user?.role === 'admin'
  }
};
