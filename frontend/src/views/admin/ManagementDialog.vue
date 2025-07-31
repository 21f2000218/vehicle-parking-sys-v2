<template>
  <div class="modal d-block" style="background: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content modal-content-enhanced">
        <div class="modal-header modal-header-enhanced">
          <h5 class="modal-title">
            <i class="bi bi-building me-2"></i>
            {{ lot.id ? 'Manage Parking Lot' : 'Add New Parking Lot' }}
          </h5>
          <button type="button" class="btn-close btn-close-white" @click="$emit('close')"></button>
        </div>
        <div class="modal-body p-4">
          <div class="row mb-4">
            <div class="col-12">
              <div class="card border-0 bg-light">
                <div class="card-header bg-primary text-white">
                  <h6 class="mb-0">
                    <i class="bi bi-info-circle me-2"></i>
                    Lot Information
                  </h6>
                </div>
                <div class="card-body">
                  <form @submit.prevent="saveLot">
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <label class="form-label-enhanced">
                          <i class="bi bi-building"></i>
                          Location Name
                        </label>
                        <input v-model="form.prime_location_name" type="text" class="form-control form-control-enhanced"
                          placeholder="Enter location name" required />
                      </div>
                      <div class="col-md-6 mb-3">
                        <label class="form-label-enhanced">
                          <i class="bi bi-geo-alt"></i>
                          Address
                        </label>
                        <input v-model="form.address" type="text" class="form-control form-control-enhanced"
                          placeholder="Enter address" required />
                      </div>
                    </div>
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <label class="form-label-enhanced">
                          <i class="bi bi-currency-rupee"></i>
                          Price per Hour
                        </label>
                        <input v-model="form.price_per_hour" type="number" step="0.01"
                          class="form-control form-control-enhanced" placeholder="Enter price" required />
                      </div>
                      <div class="col-md-6 mb-3">
                        <label class="form-label-enhanced">
                          <i class="bi bi-check-circle"></i>
                          Available Spots
                        </label>
                        <input v-model="form.available_spots" type="number" class="form-control form-control-enhanced"
                          placeholder="Number of spots" required />
                      </div>
                    </div>
                    <div class="d-flex gap-2">
                      <button type="submit" class="btn btn-enhanced btn-success-enhanced" :disabled="saving">
                        <i class="bi bi-check-circle me-2"></i>
                        {{ saving ? 'Saving...' : (lot.id ? 'Update Lot' : 'Create Lot') }}
                      </button>
                      <button type="button" class="btn btn-outline-secondary" @click="$emit('close')">
                        Cancel
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>

          <div v-if="lot.id" class="row">
            <div class="col-12">
              <div class="card border-0">
                <div class="card-header card-header-enhanced">
                  <div class="d-flex align-items-center justify-content-between">
                    <h6 class="mb-0">
                      <i class="bi bi-grid me-2"></i>
                      Parking Spots ({{ spots.length }})
                    </h6>
                    <button class="btn btn-sm btn-enhanced btn-primary-enhanced" @click="addSpot"
                      :disabled="addingSpot">
                      <i class="bi bi-plus-circle me-1"></i>
                      {{ addingSpot ? 'Adding...' : 'Add Spot' }}
                    </button>
                  </div>
                </div>
                <div class="card-body p-0">
                  <div class="table-responsive">
                    <table class="table table-enhanced table-hover mb-0">
                      <thead>
                        <tr>
                          <th class="px-4 py-3">
                            <i class="bi bi-hash me-1"></i>
                            Spot ID
                          </th>
                          <th class="py-3">
                            <i class="bi bi-info-circle me-1"></i>
                            Status
                          </th>
                          <th class="py-3 text-center">
                            <i class="bi bi-gear me-1"></i>
                            Actions
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="spot in spots" :key="spot.id" class="align-middle">
                          <td class="px-4 py-3">
                            <span class="badge bg-primary bg-opacity-10 text-primary fw-semibold">
                              {{ spot.id }}
                            </span>
                          </td>
                          <td class="py-3">
                            <span v-if="spot.status === 'occupied'" class="badge bg-danger">
                              <i class="bi bi-x-circle me-1"></i>
                              Occupied
                            </span>
                            <span v-else class="badge bg-success">
                              <i class="bi bi-check-circle me-1"></i>
                              Available
                            </span>
                          </td>
                          <td class="py-3 text-center">
                            <button class="btn btn-danger btn-sm btn-enhanced" @click="deleteSpot(spot.id)"
                              :disabled="spot.status === 'occupied' || deletingSpot === spot.id">
                              <i class="bi bi-trash"></i>
                              {{ deletingSpot === spot.id ? '...' : '' }}
                            </button>
                          </td>
                        </tr>
                        <tr v-if="spots.length === 0">
                          <td colspan="3" class="text-center py-4">
                            <div class="text-muted">
                              <i class="bi bi-grid fs-3 d-block mb-2"></i>
                              <p class="mb-0">No parking spots found</p>
                              <small>Add spots to this parking lot</small>
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
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue';
import { api } from '@/api/api';
import { toastService } from '@/utils/toastService';

export default {
  name: 'ManagementDialog',
  props: {
    lot: { type: Object, required: true }
  },
  emits: ['close', 'updated'],
  setup(props, { emit }) {
    const form = ref({
      prime_location_name: '',
      address: '',
      price_per_hour: '',
      available_spots: ''
    });
    const spots = ref([]);
    const saving = ref(false);
    const addingSpot = ref(false);
    const deletingSpot = ref(null);

    const loadLotData = () => {
      if (props.lot.id) {
        form.value = { ...props.lot };
        loadSpots();
      } else {
        form.value = {
          prime_location_name: '',
          address: '',
          price_per_hour: '',
          available_spots: ''
        };
      }
    };

    const loadSpots = async () => {
      try {
        const data = await api.getSpots(props.lot.id);
        spots.value = data;
        const availableCount = data.filter(spot => spot.status !== 'occupied').length;

        form.value.available_spots = availableCount;
      } catch (error) {
        console.error('Failed to load spots:', error);
        toastService.error('Failed to load parking spots');
      }
    };

    const saveLot = async () => {
      saving.value = true;
      try {
        const result = await api.saveLot(form.value, props.lot.id || null);

        if (result) {
          if (props.lot.id) {
            toastService.success('Parking lot updated successfully!');
          } else {
            toastService.success('Parking lot created successfully!');
          }
          emit('updated');
          emit('close');
        } else {
          toastService.error('Failed to save parking lot');
        }
      } catch (error) {
        console.error('Save lot error:', error);
        toastService.error('Failed to save parking lot');
      } finally {
        saving.value = false;
      }
    };

    const addSpot = async () => {
      addingSpot.value = true;
      try {
        const currentSpots = await api.getSpots(props.lot.id);
        const totalSpots = currentSpots.length;
        const availableSpots = currentSpots.filter(spot => spot.status !== 'occupied').length;

        const updatedData = {
          ...form.value,
          available_spots: totalSpots + 1
        };

        const result = await api.saveLot(updatedData, props.lot.id);

        if (result) {
          toastService.success('Parking spot added successfully!');
          form.value.available_spots = totalSpots + 1;
          await loadSpots();
          emit('updated');
        } else {
          toastService.error('Failed to add parking spot');
        }
      } catch (error) {
        console.error('Add spot error:', error);
        toastService.error('Failed to add parking spot');
      } finally {
        addingSpot.value = false;
      }
    };

    const deleteSpot = async (spotId) => {
      if (!confirm('Are you sure you want to delete this parking spot?')) {
        return;
      }

      deletingSpot.value = spotId;
      try {
        const success = await api.deleteSpot(spotId);
        if (success) {
          toastService.success('Parking spot deleted successfully!');
          await loadSpots();
          emit('updated');
        } else {
          toastService.error('Failed to delete parking spot');
        }
      } catch (error) {
        console.error('Delete spot error:', error);
        toastService.error('Failed to delete parking spot');
      } finally {
        deletingSpot.value = null;
      }
    };

    watch(() => props.lot, loadLotData, { immediate: true });

    return {
      form,
      spots,
      saving,
      addingSpot,
      deletingSpot,
      saveLot,
      addSpot,
      deleteSpot
    };
  }
};
</script>