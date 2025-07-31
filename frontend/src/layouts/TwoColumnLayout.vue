<template>
  <div class="layout-container">
    <Sidebar :collapsed="collapsed" :is-mobile="isMobile" @toggle="toggle" @edit-profile="handleEditProfile" />

    <div v-if="!collapsed && isMobile" class="sidebar-overlay" @click="toggle"></div>

    <div class="main-content">
      <header class="main-header">
        <button class="btn btn-outline-secondary btn-sm toggle-btn" @click="toggle">
          <i :class="collapsed ? 'bi bi-list' : 'bi bi-x'"></i>
        </button>
        <slot name="header" />
      </header>
      <main class="main-body">
        <div class="content-wrapper">
          <slot />
        </div>
      </main>
    </div>

    <EditProfileDialog v-if="showEditDialog" @close="showEditDialog = false" @profile-updated="handleProfileUpdated" />
  </div>
</template>

<script>
import Sidebar from '@/components/SideBar.vue';
import { ref, onMounted, onUnmounted } from 'vue';
import EditProfileDialog from '@/components/EditProfileDialog.vue';

export default {
  name: "TwoColumnLayout",
  components: { Sidebar, EditProfileDialog },
  props: { collapsed: Boolean },
  emits: ["toggle", "edit-profile"],
  setup(props, { emit }) {
    const isMobile = ref(false);
    const showEditDialog = ref(false);

    const handleEditProfile = () => {
      showEditDialog.value = true;
    };

    const handleProfileUpdated = () => {
      showEditDialog.value = false;

    };

    const checkMobile = () => {
      isMobile.value = window.innerWidth <= 768;
    };

    const toggle = () => emit("toggle");

    onMounted(() => {
      checkMobile();
      window.addEventListener('resize', checkMobile);
    });

    onUnmounted(() => {
      window.removeEventListener('resize', checkMobile);
    });

    return { toggle, isMobile, handleProfileUpdated, showEditDialog, handleEditProfile };
  },
};
</script>

<style scoped>
.layout-container {
  display: flex;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}


.main-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.main-header {
  background: #fff;
  border-bottom: 1px solid #dee2e6;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.toggle-btn {
  flex-shrink: 0;
}

.main-body {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  background: #f8f9fa;
  -webkit-overflow-scrolling: touch;
  position: relative;
}

.content-wrapper {
  padding: 1.5rem;
  max-width: 100%;
  margin: 0 auto;
  min-height: 100%;
}

.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}


@media (max-width: 768px) {
  .layout-container {
    display: block;
    height: 100vh;
    overflow: hidden;
  }

  .main-content {
    width: 100%;
    height: 100vh;
  }

  .main-body {
    height: calc(100vh - 70px);
    overflow-y: auto;
    overflow-x: hidden;
  }

  .content-wrapper {
    padding: 1rem;
    padding-bottom: 2rem;
  }

  .main-header {
    padding: 0.75rem 1rem;
    height: 70px;
  }
}

@media (max-width: 576px) {
  .content-wrapper {
    padding: 0.75rem;
    padding-bottom: 2rem;
  }

  .main-header {
    padding: 0.5rem 0.75rem;
    height: 60px;
  }

  .main-body {
    height: calc(100vh - 60px);
  }
}

@media (min-width: 1200px) {
  .content-wrapper {
    max-width: 1140px;
  }
}
</style>