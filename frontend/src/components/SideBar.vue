<template>
  <nav class="sidebar" :class="{
    collapsed,
    'mobile-mode': isMobile,
    'mobile-hidden': collapsed && isMobile,
  }">
    <div class="profile-section">
      <div class="profile-avatar">
        <img :src="userAvatar" alt="User Avatar" class="avatar-img"
          @error="$event.target.src = '/default-avatar.png'" />

        <div v-if="(!collapsed && !isMobile) || isMobile" class="profile-name">
          {{ user.username }}
        </div>
      </div>

      <button v-if="(!collapsed && !isMobile) || isMobile" class="btn-edit-profile" @click="$emit('edit-profile')"
        title="Edit Profile">
        <i class="bi bi-pencil"></i>
      </button>
    </div>


    <div class="nav-section">

      <div v-if="((!collapsed && !isMobile) || isMobile) && user.role" class="nav-title">
        {{ user.role === "admin" ? "ADMIN MENU" : "USER MENU" }}
      </div>

      <ul class="nav-list">
        <template v-if="user.role === 'user'">
          <li class="nav-item">
            <router-link to="/user/dashboard" class="nav-link">
              <i class="bi bi-speedometer2"></i>

              <span v-if="(!collapsed && !isMobile) || isMobile" class="nav-text">Dashboard</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/user/search" class="nav-link">
              <i class="bi bi-search"></i>
              <span v-if="(!collapsed && !isMobile) || isMobile" class="nav-text">Search</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/user/summary" class="nav-link">
              <i class="bi bi-bar-chart"></i>
              <span v-if="(!collapsed && !isMobile) || isMobile" class="nav-text">Analytics</span>
            </router-link>
          </li>
        </template>

        <template v-if="user.role === 'admin'">
          <li class="nav-item">
            <router-link to="/admin/dashboard" class="nav-link">
              <i class="bi bi-speedometer2"></i>
              <span v-if="(!collapsed && !isMobile) || isMobile" class="nav-text">Dashboard</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/management" class="nav-link">
              <i class="bi bi-gear"></i>
              <span v-if="(!collapsed && !isMobile) || isMobile" class="nav-text">Manage Lots</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/search" class="nav-link">
              <i class="bi bi-filter"></i>
              <span v-if="(!collapsed && !isMobile) || isMobile" class="nav-text">Search</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/users" class="nav-link">
              <i class="bi bi-people"></i>
              <span v-if="(!collapsed && !isMobile) || isMobile" class="nav-text">Users</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/summary" class="nav-link">
              <i class="bi bi-bar-chart"></i>
              <span v-if="(!collapsed && !isMobile) || isMobile" class="nav-text">Analytics</span>
            </router-link>
          </li>
        </template>
      </ul>
    </div>


    <div class="logout-section">
      <button @click="logout" class="nav-link logout-btn">
        <i class="bi bi-box-arrow-right"></i>
        <span v-if="(!collapsed && !isMobile) || isMobile" class="nav-text">Logout</span>
      </button>
    </div>
  </nav>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  props: {
    collapsed: Boolean,
    isMobile: Boolean,
  },
  emits: ["toggle", "edit-profile"],
  setup() {
    const store = useStore();
    const router = useRouter();

    const user = computed(() => store.getters["auth/getUser"] || {});
    const userAvatar = computed(
      () => user.value?.avatar || "/default-avatar.png"
    );

    const logout = () => {
      store.dispatch("auth/logout");
      router.push("/login");
    };

    return { user, logout, userAvatar };
  },
};
</script>

<style scoped>
.sidebar {
  height: 100vh;
  width: 240px;
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  flex-shrink: 0;
  overflow: hidden;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}


.sidebar.collapsed:not(.mobile-mode) {
  width: 60px;
}


.sidebar.mobile-mode {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.08);
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  width: 240px;
}

.sidebar.mobile-mode:not(.collapsed) {
  transform: translateX(0);
}


.profile-section {
  padding: 1.5rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-height: 80px;
  flex-shrink: 0;
}

.sidebar.collapsed:not(.mobile-mode) .profile-section {
  padding: 1rem 0.5rem;
  justify-content: center;
  gap: 0;
}

.sidebar.collapsed:not(.mobile-mode) .profile-avatar {
  justify-content: center;
  gap: 0;
}

.profile-avatar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  min-width: 0;
}

.avatar-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.profile-name {
  font-weight: 600;
  color: white;
  font-size: 0.875rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-edit-profile {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
  transition: all 0.2s;
  flex-shrink: 0;
  cursor: pointer;
}

.btn-edit-profile:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}


.nav-section {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
}

.nav-title {
  padding: 0 1rem 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 0.5rem;
}

.sidebar.collapsed:not(.mobile-mode) .nav-title {
  display: none;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin: 0;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.875rem 1rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.2s;
  border-left: 3px solid transparent;
  gap: 0.75rem;
  cursor: pointer;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
}

.sidebar.collapsed:not(.mobile-mode) .nav-link {
  padding: 0.875rem 0.5rem;
  justify-content: center;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border-left-color: #3498db;
}

.nav-link i {
  font-size: 1.125rem;
  width: 20px;
  text-align: center;
  flex-shrink: 0;
}

.nav-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}


.nav-link.router-link-active,
.nav-link.router-link-exact-active {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border-left-color: #3498db;
  font-weight: 600;
}


.logout-section {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  flex-shrink: 0;
}

.logout-btn {
  width: 100%;
  color: #e74c3c !important;
  background: rgba(231, 76, 60, 0.1);
  border: 1px solid rgba(231, 76, 60, 0.2);
  border-radius: 6px;
  justify-content: flex-start;
}

.sidebar.collapsed:not(.mobile-mode) .logout-btn {
  justify-content: center;
}

.logout-btn:hover {
  background: rgba(231, 76, 60, 0.2);
  border-color: #e74c3c;
  color: white !important;
}


.sidebar.collapsed:not(.mobile-mode) .profile-name {
  display: none;
}


.sidebar.collapsed:not(.mobile-mode) .btn-edit-profile {
  display: none;
}


@media (max-width: 768px) {
  .sidebar:not(.mobile-mode) {
    display: none;
  }
}
</style>