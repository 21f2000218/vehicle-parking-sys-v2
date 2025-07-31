<template>
  <div class="auth-container">
    <div class="auth-card fade-in">
      <div class="auth-header">
        <div class="auth-logo">
          <i class="bi bi-car-front-fill"></i>
          <h4 class="mb-0">Vehicle Parking System</h4>
        </div>
        <p class="mb-0 text-white-50">Sign in to your account</p>
      </div>

      <div class="auth-body">
        <form @submit.prevent="login" novalidate>
          <div class="mb-3">
            <label class="form-label-enhanced">
              <i class="bi bi-person"></i>
              Username <span class="text-danger">*</span>
            </label>
            <input v-model="form.username" type="text" class="form-control form-control-lg form-control-enhanced"
              :class="{ 'is-invalid': errors.username, 'is-valid': form.username && !errors.username }" required
              placeholder="Enter your username" @blur="validateUsername" @input="clearError('username')" />
            <div v-if="errors.username" class="invalid-feedback">
              {{ errors.username }}
            </div>
          </div>


          <div class="mb-3">
            <label class="form-label-enhanced">
              <i class="bi bi-lock"></i>
              Password <span class="text-danger">*</span>
            </label>
            <div class="input-group">
              <input v-model="form.password" :type="showPassword ? 'text' : 'password'"
                class="form-control form-control-lg form-control-enhanced"
                :class="{ 'is-invalid': errors.password, 'is-valid': form.password && !errors.password }" required
                placeholder="Enter your password" @blur="validatePassword" @input="clearError('password')" />
              <button type="button" class="btn btn-outline-secondary" @click="showPassword = !showPassword">
                <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
              </button>
            </div>
            <div v-if="errors.password" class="invalid-feedback d-block">
              {{ errors.password }}
            </div>
          </div>

          <button type="submit" class="btn btn-lg w-100 btn-enhanced btn-primary-enhanced mb-3"
            :disabled="loading || !isFormValid">
            <span v-if="loading" class="spinner-border spinner-border-sm"></span>
            <i v-else class="bi bi-box-arrow-in-right"></i>
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>

          <div class="text-center my-3">
            <span class="text-muted">New to the platform?</span>
          </div>

          <router-link to="/signup" class="btn btn-outline-primary btn-lg w-100">
            <i class="bi bi-person-plus me-2"></i>
            Create Account
          </router-link>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  name: "LoginPage",
  setup() {
    const store = useStore();
    const router = useRouter();
    const loading = ref(false);
    const showPassword = ref(false);

    const form = reactive({
      username: "",
      password: ""
    });

    const errors = reactive({
      username: "",
      password: ""
    });

    const validateUsername = () => {
      if (!form.username) {
        errors.username = "Username is required";
        return false;
      }
      if (form.username.length < 3) {
        errors.username = "Username must be at least 3 characters";
        return false;
      }
      errors.username = "";
      return true;
    };

    const validatePassword = () => {
      if (!form.password) {
        errors.password = "Password is required";
        return false;
      }
      if (form.password.length < 6) {
        errors.password = "Password must be at least 6 characters";
        return false;
      }
      errors.password = "";
      return true;
    };

    const clearError = (field) => {
      errors[field] = "";
    };

    const isFormValid = computed(() => {
      return form.username &&
        form.password &&
        !errors.username &&
        !errors.password;
    });

    const login = async () => {
      if (!validateUsername() || !validatePassword()) {
        return;
      }

      loading.value = true;
      try {
        await store.dispatch("auth/login", form);
        const role = store.getters["auth/getUser"].role;
        router.push(role === "admin" ? "/admin/dashboard" : "/user/dashboard");
      } catch (error) {
      } finally {
        loading.value = false;
      }
    };

    return {
      form,
      errors,
      login,
      loading,
      showPassword,
      validateUsername,
      validatePassword,
      clearError,
      isFormValid
    };
  },
};
</script>