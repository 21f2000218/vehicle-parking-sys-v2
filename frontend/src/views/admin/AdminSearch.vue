<template>
  <TwoColumnLayout :collapsed="collapsed" @toggle="toggle" @edit-profile="showEdit = true">
    <template #header>
      <div class="d-flex align-items-center">
        <i class="bi bi-search me-2 text-primary"></i>
        <h4 class="mb-0">Search Reservations</h4>
      </div>
    </template>

    <div class="container-fluid p-4">

      <div class="row mb-4">
        <div class="col-12">
          <div class="card card-enhanced border-0">
            <div class="card-header card-header-enhanced">
              <div class="d-flex align-items-center">
                <i class="bi bi-funnel me-2"></i>
                <h5 class="mb-0">Search Filters</h5>
              </div>
            </div>
            <div class="card-body p-4">
              <div class="row">
                <div class="col-md-4 mb-3">
                  <label class="form-label-enhanced">
                    <i class="bi bi-geo-alt"></i>
                    Location
                  </label>
                  <input v-model="filters.location" placeholder="Location" class="form-control form-control-enhanced" />
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label-enhanced">
                    <i class="bi bi-person"></i>
                    User ID
                  </label>
                  <input v-model="filters.user_id" placeholder="User ID" class="form-control form-control-enhanced" />
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label-enhanced">
                    <i class="bi bi-hash"></i>
                    Parking ID
                  </label>
                  <input v-model="filters.parking_id" placeholder="Parking ID"
                    class="form-control form-control-enhanced" />
                </div>
              </div>
              <button class="btn btn-enhanced btn-primary-enhanced" @click="search">
                <i class="bi bi-search me-2"></i>
                Search
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <div class="card card-enhanced border-0">
            <div class="card-header card-header-enhanced">
              <div class="d-flex align-items-center justify-content-between">
                <div class="d-flex align-items-center">
                  <i class="bi bi-list-ul me-2"></i>
                  <h5 class="mb-0">Search Results</h5>
                </div>
                <span v-if="reservations.length > 0" class="badge bg-info">
                  {{ reservations.length }} results found
                </span>
              </div>
            </div>
            <div class="card-body p-0" v-if="reservations.length">
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
                        User
                      </th>
                      <th class="py-3">
                        <i class="bi bi-car-front me-1"></i>
                        Vehicle No.
                      </th>
                      <th class="py-3">
                        <i class="bi bi-info-circle me-1"></i>
                        Status
                      </th>
                      <th class="py-3">
                        <i class="bi bi-box-arrow-in-right me-1"></i>
                        In
                      </th>
                      <th class="py-3">
                        <i class="bi bi-box-arrow-right me-1"></i>
                        Out
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="r in reservations" :key="r.id" class="align-middle">
                      <td class="px-4 py-3">
                        <span class="badge bg-primary bg-opacity-10 text-primary fw-semibold">
                          {{ r.id }}
                        </span>
                      </td>
                      <td class="py-3">
                        <div class="d-flex align-items-center">
                          <div class="bg-secondary bg-opacity-10 rounded-circle p-2 me-2">
                            <i class="bi bi-person text-secondary"></i>
                          </div>
                          <span class="fw-semibold">{{ r.user_id }}</span>
                        </div>
                      </td>
                      <td class="py-3">{{ r.vehicle_no }}</td>
                      <td class="py-3">
                        <span class="badge bg-info bg-opacity-10 text-info">
                          {{ r.status }}
                        </span>
                      </td>
                      <td class="py-3">
                        <span class="text-success fw-medium">
                          {{ format(r.parking_in_time) }}
                        </span>
                      </td>
                      <td class="py-3">
                        <span v-if="r.parking_out_time" class="text-danger fw-medium">
                          {{ r.parking_out_time }}
                        </span>
                        <span v-else class="badge bg-warning text-dark">
                          <i class="bi bi-clock me-1"></i>
                          Active
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div v-else class="card-body text-center py-5">
              <div class="text-muted">
                <i class="bi bi-search fs-1 d-block mb-3"></i>
                <h5>No data to display</h5>
                <p class="mb-0">Use the search filters above to find reservations</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </TwoColumnLayout>
</template>

<script>
import TwoColumnLayout from "@/layouts/TwoColumnLayout.vue";
import http from "@/utils/http";
import { format } from "date-fns";
import { ref } from "vue";
import { api } from "@/api/api";

export default {
  name: "AdminSearch",
  components: { TwoColumnLayout },
  setup() {
    const collapsed = ref(false);
    const showEdit = ref(false);
    const filters = ref({ location: "", user_id: "", parking_id: "" });
    const reservations = ref([]);

    const toggle = () => (collapsed.value = !collapsed.value);
    const formatDate = (dt) => format(new Date(dt), "yyyy-MM-dd HH:mm");

    const search = async () => {
      const params = {};
      Object.entries(filters.value).forEach(([k, v]) => {
        if (v) params[k] = v;
      });
      const res = await api.adminSearch(params);
      reservations.value = res;
    };

    return {
      collapsed,
      toggle,
      showEdit,
      filters,
      reservations,
      format: formatDate,
      search,
    };
  },
};
</script>