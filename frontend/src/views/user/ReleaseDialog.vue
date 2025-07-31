<template>
  <div class="modal d-block">
    <div class="modal-dialog">
      <form class="modal-content" @submit.prevent="releaseSpot">
        <div class="modal-header">
          <h5 class="modal-title">Release Reservation</h5>
          <button type="button" class="btn-close" @click="$emit('close')" />
        </div>
        <div class="modal-body">
          <div class="reservation-details mb-4">
            <h6 class="text-primary">Reservation Details</h6>
            <div class="row">
              <div class="col-sm-6">
                <strong>Reservation ID:</strong> {{ reservation.id }}
              </div>
              <div class="col-sm-6">
                <strong>Vehicle:</strong> {{ reservation.vehicle_no }}
              </div>
            </div>
            <div class="row mt-2">
              <div class="col-sm-6">
                <strong>Check-in Time:</strong><br>
                <span class="text-muted">{{ format(reservation.parking_in_time) }}</span>
              </div>
              <div class="col-sm-6">
                <strong>Duration:</strong><br>
                <span class="text-muted">{{ calculateDuration() }}</span>
              </div>
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label">
              <strong>Exit Time</strong>
              <small class="text-muted">(Auto-calculated)</small>
            </label>
            <input type="datetime-local" v-model="outTime" class="form-control" :class="{ 'bg-light': true }" readonly
              disabled required />
            <div class="form-text">
              <i class="bi bi-info-circle"></i>
              Exit time is automatically set to current time
            </div>
          </div>

          <div class="estimated-cost bg-light p-3 rounded">
            <h6 class="mb-2">
              <i class="bi bi-calculator"></i>
              Estimated Cost
            </h6>
            <div class="d-flex justify-content-between">
              <span>Duration: {{ calculateDuration() }}</span>
              <span class="text-primary fw-bold">Cost will be calculated upon release</span>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')" :disabled="loading">
            Cancel
          </button>
          <button type="submit" class="btn btn-warning" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="bi bi-box-arrow-right me-1"></i>
            {{ loading ? 'Processing...' : 'Release & Calculate Cost' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { formatISO, differenceInMinutes, format as formatDate } from "date-fns";
import { api } from "@/api/api";
import { toast } from "vue3-toastify";

export default {
  props: { reservation: { type: Object, required: true } },
  emits: ["close", "released", "payment-required"],
  setup(props, { emit }) {
    const loading = ref(false);
    const now = new Date();
    const outTime = ref(formatISO(now).slice(0, 16));


    const updateExitTime = () => {
      const currentTime = new Date();
      outTime.value = formatISO(currentTime).slice(0, 16);
    };

    onMounted(() => {

      const interval = setInterval(updateExitTime, 30000);


      return () => clearInterval(interval);
    });

    const format = (dt) => {
      return formatDate(new Date(dt), "MMM dd, yyyy HH:mm");
    };

    const calculateDuration = () => {
      const inTime = new Date(props.reservation.parking_in_time);
      const currentTime = new Date();
      const minutes = differenceInMinutes(currentTime, inTime);

      if (minutes < 60) {
        return `${minutes} minutes`;
      } else {
        const hours = Math.floor(minutes / 60);
        const remainingMinutes = minutes % 60;
        return `${hours}h ${remainingMinutes}m`;
      }
    };

    const releaseSpot = async () => {
      loading.value = true;

      try {

        const currentTime = new Date().toISOString();
        const response = await api.releaseSpot(props.reservation.id, currentTime);

        if (response && response.success) {
          const { total_cost, duration_hours, parking_fee } = response;

          toast.success("Spot released successfully!");


          emit("payment-required", {
            reservationId: props.reservation.id,
            vehicleNo: props.reservation.vehicle_no,
            totalCost: total_cost,
            durationHours: duration_hours,
            parkingFee: parking_fee,
            checkInTime: props.reservation.parking_in_time,
            checkOutTime: currentTime
          });

          emit("released");
          emit("close");
        } else {
          toast.error("Failed to release spot");
        }
      } catch (error) {
        console.error("Release error:", error);
        toast.error("Failed to release spot");
      } finally {
        loading.value = false;
      }
    };

    return {
      outTime,
      loading,
      format,
      calculateDuration,
      releaseSpot
    };
  },
};
</script>

<style scoped>
.reservation-details {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #007bff;
}

.estimated-cost {
  border-left: 4px solid #ffc107;
}

.form-control:disabled {
  background-color: #f8f9fa !important;
  opacity: 0.8;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style>