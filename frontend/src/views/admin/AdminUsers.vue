<template>
  <TwoColumnLayout :collapsed="collapsed" @toggle="toggle" @edit-profile="showEdit = true">
    <template #header>
      <div class="d-flex align-items-center">
        <i class="bi bi-people me-2 text-primary"></i>
        <h4 class="mb-0">Manage Users</h4>
      </div>
    </template>

    <div class="container-fluid p-4">
      <div class="row">
        <div class="col-12">
          <div class="card card-enhanced border-0">
            <div class="card-header card-header-enhanced">
              <div class="d-flex align-items-center justify-content-between">
                <div class="d-flex align-items-center">
                  <i class="bi bi-list-ul me-2"></i>
                  <h5 class="mb-0">Registered Users</h5>
                </div>
                <span class="badge bg-info">{{ users.length }} users</span>
              </div>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-enhanced table-hover mb-0">
                  <thead>
                    <tr>
                      <th class="px-4 py-3">
                        <i class="bi bi-hash me-1"></i>
                        ID
                      </th>
                      <th class="py-3">
                        <i class="bi bi-person me-1"></i>
                        Username
                      </th>
                      <th class="py-3">
                        <i class="bi bi-envelope me-1"></i>
                        Email
                      </th>
                      <th class="py-3">
                        <i class="bi bi-card-text me-1"></i>
                        License
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="u in users" :key="u.id" class="align-middle">
                      <td class="px-4 py-3">
                        <span class="badge bg-primary bg-opacity-10 text-primary fw-semibold">
                          {{ u.id }}
                        </span>
                      </td>
                      <td class="py-3">
                        <div class="d-flex align-items-center">
                          <div class="bg-secondary bg-opacity-10 rounded-circle p-2 me-2">
                            <i class="bi bi-person text-secondary"></i>
                          </div>
                          <span class="fw-semibold">{{ u.username }}</span>
                        </div>
                      </td>
                      <td class="py-3">{{ u.email }}</td>
                      <td class="py-3">
                        <span class="badge bg-info bg-opacity-10 text-info">
                          {{ u.license_no }}
                        </span>
                      </td>
                    </tr>
                    <tr v-if="users.length === 0">
                      <td colspan="4" class="text-center py-5">
                        <div class="text-muted">
                          <i class="bi bi-people fs-1 d-block mb-2"></i>
                          <p class="mb-0">No users found</p>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </TwoColumnLayout>
</template>

<script>
import { api } from "@/api/api";
import TwoColumnLayout from "@/layouts/TwoColumnLayout.vue";
import { onMounted, ref } from "vue";

export default {
  components: { TwoColumnLayout },
  setup() {
    const collapsed = ref(false);
    const showEdit = ref(false);
    const users = ref([]);

    const toggle = () => (collapsed.value = !collapsed.value);
    const refresh = async () => {
      users.value = await api.getAdminUsers();
    };

    onMounted(refresh);

    return { collapsed, toggle, users, showEdit };
  },
};
</script>