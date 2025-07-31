import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';
import '@/assets/styles.css';
import Toast, { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

const app = createApp(App);

app.use(Toast, {
  autoClose: 30000,
  position: 'top-right',
  pauseOnHover: true,
  theme: 'light'
});

app.config.globalProperties.$toast = toast;

app.use(router);
app.use(store);
app.mount('#app');
