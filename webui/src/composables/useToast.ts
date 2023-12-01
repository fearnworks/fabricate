import { ref } from 'vue';
import { ToastMethods } from '../types';
import ToastComponent from '@/components/ToastComponent.vue';

export default function useToast() {
  const toastRef = ref<InstanceType<typeof ToastComponent>>();

  const showToast: ToastMethods['showToast'] = (message) => {
    toastRef.value?.showToast(message);
  };

  return { showToast, toastRef };
}
