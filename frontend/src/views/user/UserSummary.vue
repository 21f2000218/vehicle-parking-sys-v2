<template>
  <TwoColumnLayout :collapsed="collapsed" @toggle="toggle" @edit-profile="showEdit = true">
    <template #header>
      <div class="d-flex align-items-center">
        <i class="bi bi-graph-up me-2 text-primary"></i>
        <h4 class="mb-0">Monthly Parking Summary</h4>
      </div>
    </template>

    <MonthlyReport mode="user" />

  </TwoColumnLayout>
</template>

<script>
import MonthlyReport from "@/components/MonthlyReport.vue";
import TwoColumnLayout from "@/layouts/TwoColumnLayout.vue";
import { ref } from "vue";

export default {
  name: "UserSummary",
  components: { TwoColumnLayout, MonthlyReport },
  setup() {
    const collapsed = ref(false);
    const showEdit = ref(false);

    const toggle = () => (collapsed.value = !collapsed.value);

    return {
      collapsed,
      toggle,
      showEdit
    };
  },
};
</script>