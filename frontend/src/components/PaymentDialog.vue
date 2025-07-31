<template>
  <div class="modal d-block">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header bg-primary text-white">
          <h5 class="modal-title">
            <i class="bi bi-credit-card me-2"></i>
            Payment Required
          </h5>
          <button type="button" class="btn-close btn-close-white" @click="$emit('close')" />
        </div>

        <div class="modal-body">

          <div class="payment-summary mb-4">
            <h6 class="text-primary mb-3">
              <i class="bi bi-receipt"></i>
              Payment Summary
            </h6>
            <div class="summary-card">
              <div class="row mb-2">
                <div class="col-6"><strong>Reservation ID:</strong></div>
                <div class="col-6">{{ paymentData.reservationId }}</div>
              </div>
              <div class="row mb-2">
                <div class="col-6"><strong>Vehicle Number:</strong></div>
                <div class="col-6">{{ paymentData.vehicleNo }}</div>
              </div>
              <div class="row mb-2">
                <div class="col-6"><strong>Duration:</strong></div>
                <div class="col-6">{{ paymentData.durationHours }} hours</div>
              </div>
              <div class="row mb-2">
                <div class="col-6"><strong>Parking Fee:</strong></div>
                <div class="col-6">₹{{ paymentData.parkingFee }}/hour</div>
              </div>
              <hr>
              <div class="row">
                <div class="col-6"><strong class="text-primary">Total Amount:</strong></div>
                <div class="col-6"><strong class="text-primary fs-5">₹{{ paymentData.totalCost }}</strong></div>
              </div>
            </div>
          </div>


          <div class="payment-methods mb-4">
            <h6 class="text-primary mb-3">
              <i class="bi bi-wallet2"></i>
              Select Payment Method
            </h6>

            <div class="row g-3">
              <div class="col-md-6">
                <div class="payment-option" :class="{ active: selectedMethod === 'card' }"
                  @click="selectMethod('card')">
                  <i class="bi bi-credit-card-2-front"></i>
                  <span>Credit/Debit Card</span>
                  <div class="check-icon" v-if="selectedMethod === 'card'">
                    <i class="bi bi-check-circle-fill"></i>
                  </div>
                </div>
              </div>

              <div class="col-md-6">
                <div class="payment-option" :class="{ active: selectedMethod === 'upi' }" @click="selectMethod('upi')">
                  <i class="bi bi-phone"></i>
                  <span>UPI</span>
                  <div class="check-icon" v-if="selectedMethod === 'upi'">
                    <i class="bi bi-check-circle-fill"></i>
                  </div>
                </div>
              </div>

              <div class="col-md-6">
                <div class="payment-option" :class="{ active: selectedMethod === 'wallet' }"
                  @click="selectMethod('wallet')">
                  <i class="bi bi-wallet"></i>
                  <span>Digital Wallet</span>
                  <div class="check-icon" v-if="selectedMethod === 'wallet'">
                    <i class="bi bi-check-circle-fill"></i>
                  </div>
                </div>
              </div>

              <div class="col-md-6">
                <div class="payment-option" :class="{ active: selectedMethod === 'cash' }"
                  @click="selectMethod('cash')">
                  <i class="bi bi-cash"></i>
                  <span>Cash Payment</span>
                  <div class="check-icon" v-if="selectedMethod === 'cash'">
                    <i class="bi bi-check-circle-fill"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>


          <div v-if="selectedMethod && selectedMethod !== 'cash'" class="payment-form mb-4">
            <h6 class="text-primary mb-3">
              <i class="bi bi-shield-lock"></i>
              Payment Details
            </h6>


            <div v-if="selectedMethod === 'card'" class="card-form">
              <div class="mb-3">
                <label class="form-label">Card Number</label>
                <input v-model="cardDetails.number" type="text" class="form-control" placeholder="1234 5678 9012 3456"
                  maxlength="19" @input="formatCardNumber" />
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Expiry Date</label>
                  <input v-model="cardDetails.expiry" type="text" class="form-control" placeholder="MM/YY" maxlength="5"
                    @input="formatExpiry" />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">CVV</label>
                  <input v-model="cardDetails.cvv" type="text" class="form-control" placeholder="123" maxlength="3" />
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Cardholder Name</label>
                <input v-model="cardDetails.name" type="text" class="form-control" placeholder="John Doe" />
              </div>
            </div>


            <div v-if="selectedMethod === 'upi'" class="upi-form">
              <div class="mb-3">
                <label class="form-label">UPI ID</label>
                <input v-model="upiId" type="text" class="form-control" placeholder="yourname@paytm" />
              </div>
            </div>


            <div v-if="selectedMethod === 'wallet'" class="wallet-form">
              <div class="mb-3">
                <label class="form-label">Select Wallet</label>
                <select v-model="selectedWallet" class="form-select">
                  <option value="">Choose wallet...</option>
                  <option value="paytm">Paytm</option>
                  <option value="phonepe">PhonePe</option>
                  <option value="googlepay">Google Pay</option>
                  <option value="amazonpay">Amazon Pay</option>
                </select>
              </div>
            </div>
          </div>


          <div v-if="selectedMethod === 'cash'" class="cash-payment-info">
            <div class="alert alert-info">
              <i class="bi bi-info-circle me-2"></i>
              <strong>Cash Payment Selected</strong><br>
              Please proceed to the payment counter to complete your payment.
              <br><br>
              <strong>Amount to Pay: ₹{{ paymentData.totalCost }}</strong>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">
            Cancel
          </button>
          <button type="button" class="btn btn-success" :disabled="!canProceed || processing" @click="processPayment">
            <span v-if="processing" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="bi bi-lock-fill me-1"></i>
            {{ processing ? 'Processing...' : `Pay ₹${paymentData.totalCost}` }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { toast } from 'vue3-toastify';

export default {
  name: 'PaymentDialog',
  props: {
    paymentData: {
      type: Object,
      required: true
    }
  },
  emits: ['close', 'payment-success'],
  setup(props, { emit }) {
    const selectedMethod = ref('');
    const processing = ref(false);


    const cardDetails = ref({
      number: '',
      expiry: '',
      cvv: '',
      name: ''
    });


    const upiId = ref('');


    const selectedWallet = ref('');

    const selectMethod = (method) => {
      selectedMethod.value = method;
    };

    const formatCardNumber = (event) => {
      let value = event.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
      let formattedValue = value.match(/.{1,4}/g)?.join(' ') || '';
      if (formattedValue.length > 19) formattedValue = formattedValue.substring(0, 19);
      cardDetails.value.number = formattedValue;
    };

    const formatExpiry = (event) => {
      let value = event.target.value.replace(/\D/g, '');
      if (value.length >= 2) {
        value = value.substring(0, 2) + '/' + value.substring(2, 4);
      }
      cardDetails.value.expiry = value;
    };

    const canProceed = computed(() => {
      if (!selectedMethod.value) return false;

      if (selectedMethod.value === 'card') {
        return cardDetails.value.number.length === 19 &&
          cardDetails.value.expiry.length === 5 &&
          cardDetails.value.cvv.length === 3 &&
          cardDetails.value.name.trim().length > 0;
      }

      if (selectedMethod.value === 'upi') {
        return upiId.value.includes('@') && upiId.value.length > 5;
      }

      if (selectedMethod.value === 'wallet') {
        return selectedWallet.value !== '';
      }

      if (selectedMethod.value === 'cash') {
        return true;
      }

      return false;
    });

    const processPayment = async () => {
      processing.value = true;


      await new Promise(resolve => setTimeout(resolve, 2000));

      try {
        const success = Math.random() > 0.1;

        if (success) {
          const paymentResult = {
            success: true,
            transactionId: `TXN${Date.now()}${Math.floor(Math.random() * 1000)}`,
            method: selectedMethod.value,
            amount: props.paymentData.totalCost,
            timestamp: new Date().toISOString(),
            reservationId: props.paymentData.reservationId
          };

          toast.success(`Payment successful! Transaction ID: ${paymentResult.transactionId}`);
          emit('payment-success', paymentResult);
          emit('close');
        } else {
          toast.error('Payment failed. Please try again.');
        }
      } catch (error) {
        toast.error('Payment processing error. Please try again.');
      } finally {
        processing.value = false;
      }
    };

    return {
      selectedMethod,
      processing,
      cardDetails,
      upiId,
      selectedWallet,
      selectMethod,
      formatCardNumber,
      formatExpiry,
      canProceed,
      processPayment
    };
  }
};
</script>

<style scoped>
.summary-card {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #007bff;
}

.payment-option {
  background: #fff;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  height: 100px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.payment-option:hover {
  border-color: #007bff;
  background: #f8f9fa;
}

.payment-option.active {
  border-color: #007bff;
  background: #e7f3ff;
  color: #007bff;
}

.payment-option i {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.payment-option span {
  font-weight: 600;
  font-size: 0.875rem;
}

.check-icon {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  color: #28a745;
}

.payment-form {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #28a745;
}

.cash-payment-info {
  text-align: center;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

.form-control:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
</style>