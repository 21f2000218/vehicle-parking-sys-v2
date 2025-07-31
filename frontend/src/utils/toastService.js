import { toast } from 'vue3-toastify';

class ToastService {
  constructor() {
    this.activeToasts = new Set();
    this.debounceTime = 3000; 
  }

  show(type, message, options = {}) {
    const key = `${type}:${message}`;
    
    if (this.activeToasts.has(key)) {
      return;
    }

    this.activeToasts.add(key);
    
    const toastOptions = {
      autoClose: options.autoClose || 3000,
      onClose: () => {
        setTimeout(() => {
          this.activeToasts.delete(key);
        }, this.debounceTime);
      },
      ...options
    };

    switch(type) {
      case 'success':
        return toast.success(message, toastOptions);
      case 'error':
        return toast.error(message, toastOptions);
      case 'warning':
        return toast.warning(message, toastOptions);
      case 'info':
        return toast.info(message, toastOptions);
    }
  }

  success(message, options = {}) {
    return this.show('success', message, options);
  }

  error(message, options = {}) {
    return this.show('error', message, options);
  }

  warning(message, options = {}) {
    return this.show('warning', message, options);
  }

  info(message, options = {}) {
    return this.show('info', message, options);
  }

  clear() {
    this.activeToasts.clear();
  }
}

export const toastService = new ToastService();