<template>
  <TwoColumnLayout :collapsed="collapsed" @toggle="toggleSidebar" @edit-profile="showEdit = true">
    <template #header>
      <div class="d-flex align-items-center">
        <i class="bi bi-speedometer2 me-2 text-primary"></i>
        <h4 class="mb-0">User Dashboard</h4>
      </div>
    </template>

    <div class="container-fluid p-4">
      <div class="row mb-4">
        <div class="col-12">
          <div class="card card-enhanced border-0">
            <div class="card-body p-4">
              <div class="d-flex align-items-center">
                <div class="bg-primary bg-opacity-10 rounded-circle p-3 me-3">
                  <i class="bi bi-person-circle fs-2 text-primary"></i>
                </div>
                <div>
                  <h5 class="mb-1">Welcome back!</h5>
                  <p class="text-muted mb-0">Manage your parking reservations</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <div class="card card-enhanced border-0">
            <div class="card-header card-header-enhanced">
              <div class="d-flex align-items-center">
                <i class="bi bi-clock-history me-2"></i>
                <h5 class="mb-0">Reservation History</h5>
              </div>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-enhanced table-hover mb-0">
                  <thead>
                    <tr>
                      <th class="px-4 py-3">
                        <i class="bi bi-hash me-1"></i>
                        Lot
                      </th>
                      <th class="py-3">
                        <i class="bi bi-car-front me-1"></i>
                        Vehicle
                      </th>
                      <th class="py-3">
                        <i class="bi bi-box-arrow-in-right me-1"></i>
                        Check In
                      </th>
                      <th class="py-3">
                        <i class="bi bi-box-arrow-right me-1"></i>
                        Check Out
                      </th>
                      <th class="py-3 text-center">
                        <i class="bi bi-gear me-1"></i>
                        Action
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="r in history" :key="r.id" class="align-middle">
                      <td class="px-4 py-3">
                        <span class="badge bg-primary bg-opacity-10 text-primary fw-semibold">
                          #{{ r.id }}
                        </span>
                      </td>
                      <td class="py-3">
                        <div class="d-flex align-items-center">
                          <div class="bg-secondary bg-opacity-10 rounded p-2 me-2">
                            <i class="bi bi-car-front text-secondary"></i>
                          </div>
                          <span class="fw-semibold">{{ r.vehicle_no }}</span>
                        </div>
                      </td>
                      <td class="py-3">
                        <span class="text-success fw-medium">
                          {{ formatDate(r.parking_in_time) }}
                        </span>
                      </td>
                      <td class="py-3">
                        <span v-if="r.parking_out_time" class="text-danger fw-medium">
                          {{ formatDate(r.parking_out_time) }}
                        </span>
                        <span v-else class="badge bg-warning text-dark">
                          <i class="bi bi-clock me-1"></i>
                          Active
                        </span>
                      </td>
                      <td class="py-3 text-center">
                        <button v-if="!r.parking_out_time" class="btn btn-warning btn-sm btn-enhanced"
                          @click="openRelease(r)">
                          <i class="bi bi-box-arrow-right me-1"></i>
                          Release
                        </button>
                        <span v-else class="text-muted">
                          <i class="bi bi-check-circle me-1"></i>
                          Completed
                        </span>
                      </td>
                    </tr>
                    <tr v-if="history.length === 0">
                      <td colspan="5" class="text-center py-5">
                        <div class="text-muted">
                          <i class="bi bi-inbox fs-1 d-block mb-2"></i>
                          <p class="mb-0">No reservations found</p>
                          <small>Your parking history will appear here</small>
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

    <ReleaseDialog v-if="active" :reservation="active" @close="onReleaseClose" @released="loadHistory"
      @payment-required="showPaymentDialog" />

    <PaymentDialog v-if="showPayment && paymentData" :payment-data="paymentData" @close="hidePaymentDialog"
      @payment-success="handlePaymentSuccess" />
  </TwoColumnLayout>
</template>

<script>
import { ref, onMounted } from "vue";
import TwoColumnLayout from "@/layouts/TwoColumnLayout.vue";
import { format } from "date-fns";
import ReleaseDialog from "./ReleaseDialog.vue";
import { api } from "@/api/api";
import PaymentDialog from "@/components/PaymentDialog.vue";
import { toastService } from "@/utils/toastService";

export default {
  name: "UserDashboard",
  components: { TwoColumnLayout, ReleaseDialog, PaymentDialog },
  setup() {
    const collapsed = ref(false);
    const history = ref([]);
    const active = ref(null);
    const showEdit = ref(false);
    const showPayment = ref(false);
    const paymentData = ref(null);

    const toggleSidebar = () => (collapsed.value = !collapsed.value);

    const loadHistory = async () => {
      const res = await api.getUserHistory();
      history.value = res;
    };

    const openRelease = (resv) => {
      active.value = resv;
    };

    const onReleaseClose = () => {
      active.value = null;
      loadHistory();
    };

    const showPaymentDialog = (data) => {
      paymentData.value = data;
      showPayment.value = true;
    };

    const hidePaymentDialog = () => {
      showPayment.value = false;
      paymentData.value = null;
    };

    const handlePaymentSuccess = (result) => {
      toastService.success(
        `Payment completed successfully! Transaction: ${result.transactionId}`
      );
      loadHistory();
      hidePaymentDialog();
    };

    const formatDate = (dt) => format(new Date(dt), "yyyy-MM-dd HH:mm");

    onMounted(loadHistory);

    return {
      collapsed,
      toggleSidebar,
      history,
      active,
      openRelease,
      onReleaseClose,
      showEdit,
      formatDate,
      handlePaymentSuccess,
      showPaymentDialog,
      hidePaymentDialog,
      showPayment,
      paymentData,
    };
  },
};
</script>

<style scoped>
.btn-enhanced {
  border-radius: var(--border-radius);
  font-weight: var(--font-weight-semibold);
  transition: var(--transition);
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.btn-enhanced:hover {
  transform: translateY(-1px);
}

.table-enhanced tbody tr:hover {
  background-color: rgba(0, 123, 255, 0.05);
}

.badge {
  font-size: 0.85rem;
}
</style>