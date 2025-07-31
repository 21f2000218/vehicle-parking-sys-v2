<template>
  <TwoColumnLayout :collapsed="collapsed" @toggle="toggle" @edit-profile="showEdit = true">
    <template #header>
      <div class="d-flex align-items-center">
        <i class="bi bi-speedometer2 me-2 text-primary"></i>
        <h4 class="mb-0">Admin Dashboard</h4>
      </div>
    </template>

    <div class="container-fluid p-2 p-md-4">
      <div class="row mb-3 mb-md-4">
        <div class="col-12">
          <div class="card card-enhanced border-0">
            <div class="card-header card-header-enhanced">
              <div class="d-flex align-items-center">
                <i class="bi bi-building me-2"></i>
                <h5 class="mb-0 fs-6 fs-md-5">Parking Lots</h5>
              </div>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-enhanced table-hover mb-0">
                  <thead>
                    <tr>
                      <th class="px-2 px-md-4 py-2 py-md-3">
                        <i class="bi bi-building me-1"></i>
                        <span class="d-none d-sm-inline">Name</span>
                        <span class="d-sm-none">Lot</span>
                      </th>
                      <th class="py-2 py-md-3 d-none d-md-table-cell">
                        <i class="bi bi-geo-alt me-1"></i>
                        Address
                      </th>
                      <th class="py-2 py-md-3">
                        <i class="bi bi-check-circle me-1"></i>
                        <span class="d-none d-sm-inline">Available</span>
                        <span class="d-sm-none">Spots</span>
                      </th>
                      <th class="py-2 py-md-3 text-center">
                        <i class="bi bi-gear me-1"></i>
                        <span class="d-none d-sm-inline">Action</span>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="lot in lots" :key="lot.id" class="align-middle">
                      <td class="px-2 px-md-4 py-2 py-md-3">
                        <div class="d-flex align-items-center">
                          <div class="bg-primary bg-opacity-10 rounded p-1 p-md-2 me-1 me-md-2">
                            <i class="bi bi-building text-primary small"></i>
                          </div>
                          <div class="flex-grow-1">
                            <div class="fw-semibold small">
                              {{ lot.prime_location_name }}
                            </div>
                            <!-- Show address on mobile under name -->
                            <div class="d-md-none">
                              <small class="text-muted">{{ lot.address }}</small>
                            </div>
                          </div>
                        </div>
                      </td>
                      <td class="py-2 py-md-3 d-none d-md-table-cell">{{ lot.address }}</td>
                      <td class="py-2 py-md-3">
                        <span class="badge bg-success bg-opacity-10 text-success">
                          <i class="bi bi-car-front me-1"></i>
                          {{ lot.available_spots }}
                        </span>
                      </td>
                      <td class="py-2 py-md-3 text-center">
                        <button class="btn btn-sm btn-enhanced btn-primary-enhanced" @click="activeLot = lot">
                          <i class="bi bi-gear me-1"></i>
                          <span class="d-none d-sm-inline">Manage</span>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Occupied Spots Section -->
      <div class="row mb-3 mb-md-4">
        <div class="col-12">
          <div class="card card-enhanced border-0">
            <div class="card-header card-header-enhanced">
              <div class="d-flex align-items-center">
                <i class="bi bi-car-front me-2"></i>
                <h5 class="mb-0 fs-6 fs-md-5">Occupied Spots</h5>
              </div>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-enhanced table-striped mb-0">
                  <thead>
                    <tr>
                      <th class="px-2 px-md-4 py-2 py-md-3">
                        <i class="bi bi-hash me-1"></i>
                        Spot ID
                      </th>
                      <th class="py-2 py-md-3">
                        <i class="bi bi-building me-1"></i>
                        Lot ID
                      </th>
                      <th class="py-2 py-md-3 d-none d-sm-table-cell">
                        <i class="bi bi-clock me-1"></i>
                        Last Updated
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="s in occupied" :key="s.id" class="align-middle">
                      <td class="px-2 px-md-4 py-2 py-md-3">
                        <span class="badge bg-warning bg-opacity-10 text-warning fw-semibold">
                          {{ s.id }}
                        </span>
                      </td>
                      <td class="py-2 py-md-3">
                        <span class="badge bg-info bg-opacity-10 text-info">
                          {{ s.lot_id }}
                        </span>
                        <!-- Show last updated on mobile under lot ID -->
                        <div class="d-sm-none">
                          <small class="text-muted d-block mt-1">{{ s.last_updated }}</small>
                        </div>
                      </td>
                      <td class="py-2 py-md-3 d-none d-sm-table-cell">{{ s.last_updated }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <ManagementDialog v-if="activeLot" :lot="activeLot" @close="closeManage" @updated="refresh" />
  </TwoColumnLayout>
</template>

<script>
import { api } from "@/api/api";
import MonthlyReport from "@/components/MonthlyReport.vue";
import TwoColumnLayout from "@/layouts/TwoColumnLayout.vue";
import ManagementDialog from "@/views/admin/ManagementDialog.vue";
import { onMounted, ref } from "vue";

export default {
  components: { TwoColumnLayout, ManagementDialog, MonthlyReport },
  setup() {
    const collapsed = ref(false);
    const showEdit = ref(false);
    const lots = ref([]);
    const occupied = ref([]);
    const activeLot = ref(null);

    const toggle = () => (collapsed.value = !collapsed.value);
    const refresh = async () => {

      lots.value = await api.getParkingLots();
      console.log(lots.value)
      occupied.value = await api.getOccupiedSpots();
    };

    const closeManage = () => {
      activeLot.value = null;
      refresh();
    };

    onMounted(refresh);

    return {
      collapsed,
      toggle,
      lots,
      occupied,
      activeLot,
      closeManage,
      showEdit,
    };
  },
};
</script>