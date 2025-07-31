<template>
  <div class="auth-container">
    <div class="auth-card fade-in">
      <div class="auth-header">
        <div class="auth-logo">
          <i class="bi bi-person-plus-fill"></i>
          <h4 class="mb-0">Create Account</h4>
        </div>
        <p class="mb-0 text-white-50">Join our parking platform</p>
      </div>
      <div class="auth-body auth-body-scrollable">
        <form @submit.prevent="register">
          <div class="row mb-3">
            <div class="col-md-6 mb-3 mb-md-0">
              <label class="form-label-enhanced">
                <i class="bi bi-person"></i>
                Username
              </label>
              <input v-model="form.username" type="text" class="form-control form-control-enhanced"
                placeholder="Enter username" required />
            </div>
            <div class="col-md-6">
              <label class="form-label-enhanced">
                <i class="bi bi-envelope"></i>
                Email
              </label>
              <input v-model="form.email" type="email" class="form-control form-control-enhanced"
                placeholder="Enter email" required />
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6 mb-3 mb-md-0">
              <label class="form-label-enhanced">
                <i class="bi bi-lock"></i>
                Password
              </label>
              <input v-model="form.password" type="password" class="form-control form-control-enhanced"
                placeholder="Enter password" required />
            </div>
            <div class="col-md-6">
              <label class="form-label-enhanced">
                <i class="bi bi-card-text"></i>
                License Number
              </label>
              <input v-model="form.license_no" type="text" class="form-control form-control-enhanced"
                placeholder="Enter license number" required />
            </div>
          </div>

          <div class="mb-4">
            <label class="form-label-enhanced">
              <i class="bi bi-shield-check"></i>
              Role
            </label>
            <select v-model="form.role" class="form-select form-select-enhanced">
              <option value="user">User</option>
            </select>
          </div>

          <button type="submit" class="btn btn-lg w-100 btn-enhanced btn-success-enhanced mb-3">
            <i class="bi bi-person-check"></i>
            Register
          </button>

          <div class="text-center">
            <router-link to="/login" class="text-primary text-decoration-none fw-semibold">
              <i class="bi bi-arrow-left me-1"></i>
              Back to Login
            </router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  name: "SignupPage",
  setup() {
    const store = useStore();
    const router = useRouter();
    const form = reactive({
      username: "",
      email: "",
      password: "",
      license_no: "",
      role: "user",
    });

    const register = async () => {
      await store.dispatch("auth/register", form);
      router.push("/user/dashboard");
    };

    return { form, register };
  },
};
</script>

<style scoped>
.auth-body-scrollable {
  max-height: calc(100vh - 140px);
  overflow-y: auto;
  overflow-x: hidden;
}

.auth-body-scrollable {
  scroll-behavior: smooth;
}

.auth-body-scrollable::-webkit-scrollbar {
  width: 6px;
}

.auth-body-scrollable::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.auth-body-scrollable::-webkit-scrollbar-thumb {
  background: #007bff;
  border-radius: 3px;
}

.auth-body-scrollable::-webkit-scrollbar-thumb:hover {
  background: #0056b3;
}

@media (max-width: 575.98px) {
  .auth-body-scrollable {
    max-height: calc(100vh - 120px);
    padding: 1rem !important;
  }

  .row.mb-3 {
    margin-bottom: 1rem !important;
  }

  .mb-4 {
    margin-bottom: 1.5rem !important;
  }

  .col-md-6 {
    margin-bottom: 1rem;
  }

  .col-md-6:last-child {
    margin-bottom: 0;
  }
}

@media (max-width: 767.98px) and (orientation: landscape) {
  .auth-body-scrollable {
    max-height: calc(100vh - 100px);
  }
}

@media (max-height: 600px) {
  .auth-body-scrollable {
    max-height: calc(100vh - 100px);
  }
}
</style>
