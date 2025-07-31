<template>
  <TwoColumnLayout :collapsed="collapsed" @toggle="toggle" @edit-profile="showEdit = true">
    <template #header>
      <div class="d-flex align-items-center">
        <i class="bi bi-building me-2 text-primary"></i>
        <h4 class="mb-0">Manage Lots & Spots</h4>
      </div>
    </template>

    <div class="container-fluid p-4">
      <button class="btn btn-enhanced btn-success-enhanced mb-3" @click="activeLot = {}">
        <i class="bi bi-plus-circle me-2"></i>
        Add New Lot
      </button>

      <div class="card card-enhanced border-0">
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
                    <i class="bi bi-building me-1"></i>
                    Name
                  </th>
                  <th class="py-3">
                    <i class="bi bi-check-circle me-1"></i>
                    Available
                  </th>
                  <th class="py-3 text-center">
                    <i class="bi bi-gear me-1"></i>
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="lot in lots" :key="lot.id" class="align-middle">
                  <td class="px-4 py-3">
                    <span class="badge bg-primary bg-opacity-10 text-primary fw-semibold">
                      {{ lot.id }}
                    </span>
                  </td>
                  <td class="py-3">
                    <div class="d-flex align-items-center">
                      <div class="bg-info bg-opacity-10 rounded p-2 me-2">
                        <i class="bi bi-building text-info"></i>
                      </div>
                      <span class="fw-semibold">{{ lot.prime_location_name }}</span>
                    </div>
                  </td>
                  <td class="py-3">
                    <span class="badge bg-success bg-opacity-10 text-success">
                      <i class="bi bi-car-front me-1"></i>
                      {{ lot.available_spots }}
                    </span>
                  </td>
                  <td class="py-3 text-center">
                    <button class="btn btn-sm btn-enhanced btn-primary-enhanced" @click="activeLot = lot">
                      <i class="bi bi-pencil me-1"></i>
                      Edit
                    </button>
                  </td>
                </tr>
                <tr v-if="lots.length === 0">
                  <td colspan="4" class="text-center py-5">
                    <div class="text-muted">
                      <i class="bi bi-inbox fs-1 d-block mb-2"></i>
                      <p class="mb-0">No parking lots found</p>
                      <small>Add a new parking lot to get started</small>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <ManagementDialog v-if="activeLot" :lot="activeLot" @close="close" @updated="refresh" />
  </TwoColumnLayout>
</template>

<script>
import { api } from "@/api/api";
import TwoColumnLayout from "@/layouts/TwoColumnLayout.vue";
import ManagementDialog from "@/views/admin/ManagementDialog.vue";
import { onMounted, ref } from "vue";

export default {
  components: { TwoColumnLayout, ManagementDialog },
  setup() {
    const collapsed = ref(false);
    const showEdit = ref(false);
    const lots = ref([]);
    const activeLot = ref(null);

    const toggle = () => (collapsed.value = !collapsed.value);
    const refresh = async () => {
      lots.value = await api.getParkingLots();
    };

    const close = () => {
      activeLot.value = null;
      refresh();
    };

    onMounted(refresh);

    return { collapsed, toggle, lots, activeLot, close, showEdit };
  },
};
</script>