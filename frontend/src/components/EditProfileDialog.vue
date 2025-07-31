<template>
  <div class="modal d-block" style="background: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content modal-content-enhanced">
        <div class="modal-header modal-header-enhanced">
          <h5 class="modal-title">
            <i class="bi bi-person-gear me-2"></i>
            Edit Profile
          </h5>
          <button type="button" class="btn-close btn-close-white" @click="$emit('close')"></button>
        </div>
        <form @submit.prevent="saveProfile">
          <div class="modal-body p-4">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label-enhanced">
                  <i class="bi bi-person"></i>
                  Username
                </label>
                <input v-model="form.username" type="text" class="form-control form-control-enhanced"
                  placeholder="Enter username" required />
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label-enhanced">
                  <i class="bi bi-envelope"></i>
                  Email Address
                </label>
                <input v-model="form.email" type="email" class="form-control form-control-enhanced"
                  placeholder="Enter email address" required />
              </div>
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label-enhanced">
                  <i class="bi bi-credit-card"></i>
                  License Number
                </label>
                <input v-model="form.license_no" type="text" class="form-control form-control-enhanced"
                  placeholder="Enter license number" required />
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label-enhanced">
                  <i class="bi bi-lock"></i>
                  Password
                  <small class="text-muted ms-1">(leave blank to keep current)</small>
                </label>
                <input v-model="form.password" type="password" class="form-control form-control-enhanced"
                  placeholder="Enter new password" />
              </div>
            </div>


            <div class="card border-0 bg-light mt-3">
              <div class="card-header bg-primary text-white">
                <h6 class="mb-0">
                  <i class="bi bi-info-circle me-2"></i>
                  Profile Summary
                </h6>
              </div>
              <div class="card-body">
                <div class="row">
                  <div class="col-sm-6">
                    <small class="text-muted">Current Username:</small>
                    <div class="fw-semibold">{{ form.username || 'Not set' }}</div>
                  </div>
                  <div class="col-sm-6">
                    <small class="text-muted">Current Email:</small>
                    <div class="fw-semibold">{{ form.email || 'Not set' }}</div>
                  </div>
                </div>
                <div class="row mt-2">
                  <div class="col-sm-6">
                    <small class="text-muted">License Number:</small>
                    <div class="fw-semibold">{{ form.license_no || 'Not set' }}</div>
                  </div>
                  <div class="col-sm-6">
                    <small class="text-muted">Password:</small>
                    <div class="fw-semibold">
                      <i class="bi bi-shield-check text-success"></i>
                      Protected
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer border-top">
            <button type="button" class="btn btn-outline-secondary" @click="$emit('close')" :disabled="saving">
              <i class="bi bi-x-circle me-1"></i>
              Cancel
            </button>
            <button type="submit" class="btn btn-enhanced btn-success-enhanced" :disabled="saving">
              <i class="bi bi-check-circle me-1"></i>
              {{ saving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { api } from "@/api/api";
import { toastService } from "@/utils/toastService";
import { onMounted, reactive, ref } from "vue";

export default {
  name: "EditProfileDialog",
  emits: ["close", "profile-updated"],
  setup(_, { emit }) {
    const saving = ref(false);
    const form = reactive({
      username: "",
      email: "",
      license_no: "",
      password: "",
    });

    const loadProfile = async () => {
      try {
        const res = await api.getProfile();
        if (!res) {
          toastService.error("Failed to load profile");
          return;
        }
        Object.assign(form, res);
        form.password = "";
      } catch (error) {
        console.error('Failed to load profile:', error);
        toastService.error("Failed to load profile data");
      }
    };

    const saveProfile = async () => {
      saving.value = true;
      try {

        const payload = {
          username: form.username,
          email: form.email,
          license_no: form.license_no,
        };


        if (form.password && form.password.trim()) {
          payload.password = form.password;
        }

        const res = await api.saveProfile(payload);

        if (res) {
          toastService.success("Profile updated successfully!");
          emit("profile-updated", res);
          emit("close");
        } else {
          toastService.error("Failed to update profile");
        }
      } catch (error) {
        console.error('Save profile error:', error);
        toastService.error("Failed to update profile");
      } finally {
        saving.value = false;
      }
    };

    onMounted(loadProfile);

    return {
      form,
      saving,
      saveProfile
    };
  },
};
</script>

<style scoped>
.modal-footer {
  background: #f8f9fa;
  border-radius: 0 0 var(--border-radius-lg) var(--border-radius-lg);
}

@media (max-width: 768px) {
  .modal-dialog {
    margin: 1rem;
  }

  .modal-body {
    padding: 1.5rem !important;
  }
}
</style>