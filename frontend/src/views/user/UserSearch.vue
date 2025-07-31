<template>
  <TwoColumnLayout :collapsed="collapsed" @toggle="toggle" @edit-profile="toggleProfile">
    <template #header>
      <div class="d-flex align-items-center">
        <i class="bi bi-search me-2 text-primary"></i>
        <h4 class="mb-0">Search Parking Lots</h4>
      </div>
    </template>

    <div class="container-fluid p-4">
      <!-- Search Form -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card card-enhanced border-0">
            <div class="card-body p-4">
              <div class="row">
                <div class="col-md-8 mb-3 mb-md-0">
                  <label class="form-label-enhanced">
                    <i class="bi bi-geo-alt"></i>
                    Location
                  </label>
                  <input v-model="search" placeholder="Enter location..." class="form-control form-control-enhanced" />
                </div>
                <div class="col-md-4 d-flex align-items-end">
                  <button class="btn btn-enhanced btn-primary-enhanced w-100" @click="loadLots">
                    <i class="bi bi-search me-2"></i>
                    Search
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Results -->
      <div class="row">
        <div class="col-12">
          <div v-for="lot in lots" :key="lot.id" class="card card-enhanced border-0 mb-3">
            <div class="card-body p-4">
              <div class="row align-items-center">
                <div class="col-md-8">
                  <h5 class="mb-2">{{ lot.prime_location_name }}</h5>
                  <p class="text-muted mb-2">
                    <i class="bi bi-geo-alt me-1"></i>
                    {{ lot.address }}
                  </p>
                  <div class="d-flex gap-3">
                    <span class="badge bg-primary bg-opacity-10 text-primary">
                      <i class="bi bi-currency-rupee me-1"></i>
                      ₹{{ lot.price_per_hour }}/hr
                    </span>
                    <span class="badge bg-success bg-opacity-10 text-success">
                      <i class="bi bi-check-circle me-1"></i>
                      Available: {{ lot.available_spots }}
                    </span>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="mb-2">
                    <label class="form-label-enhanced">
                      <i class="bi bi-car-front"></i>
                      Vehicle Number
                    </label>
                    <input v-model="vehicle_no" class="form-control form-control-enhanced"
                      placeholder="Enter Vehicle No" />
                  </div>
                  <button class="btn btn-enhanced btn-success-enhanced w-100" @click="bookSpot(lot.id)">
                    <i class="bi bi-bookmark-plus me-2"></i>
                    Book Spot
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- No Results -->
      <div v-if="lots.length === 0" class="row">
        <div class="col-12">
          <div class="card card-enhanced border-0">
            <div class="card-body text-center py-5">
              <div class="text-muted">
                <i class="bi bi-search fs-1 d-block mb-3"></i>
                <h5>Search for Parking Lots</h5>
                <p class="mb-0">Enter a location to find available parking spots</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </TwoColumnLayout>
</template>

<script>
import { ref } from "vue";
import http from "@/utils/http";
import TwoColumnLayout from "@/layouts/TwoColumnLayout.vue";
import { api } from "@/api/api";
import { toastService } from "@/utils/toastService";

export default {
  name: "UserSearch",
  components: { TwoColumnLayout },
  setup() {
    const collapsed = ref(false);
    const search = ref("");
    const lots = ref([]);
    const vehicle_no = ref("");

    const toggle = () => (collapsed.value = !collapsed.value);
    const toggleProfile = () => { };

    const loadLots = async () => {
      const res = await api.getAvailableLots(search.value)
      lots.value = res;
    };

    const bookSpot = async (lot_id) => {
      await api.bookSpot(lot_id, vehicle_no.value)
      toastService.success("Booking confirmed!");
    };

    return {
      collapsed,
      toggle,
      toggleProfile,
      search,
      lots,
      vehicle_no,
      loadLots,
      bookSpot,
    };
  },
};
</script>