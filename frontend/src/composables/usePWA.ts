import { ref, onMounted } from 'vue';
import { useRegisterSW } from 'virtual:pwa-register/vue';

export function usePWA() {
  const needRefresh = ref(false);
  const updateServiceWorker = ref<(() => Promise<void>) | undefined>();

  const {
    needRefresh: swNeedRefresh,
    updateServiceWorker: swUpdateServiceWorker,
  } = useRegisterSW({
    onRegistered(registration: ServiceWorkerRegistration | undefined) {
      console.log('Service Worker registered:', registration);

      // Check for updates every hour
      setInterval(() => {
        registration?.update();
      }, 60 * 60 * 1000);
    },
    onRegisterError(error: Error) {
      console.error('Service Worker registration error:', error);
    },
    onNeedRefresh() {
      needRefresh.value = true;
    },
  });

  // Sync refs
  onMounted(() => {
    needRefresh.value = swNeedRefresh.value;
    updateServiceWorker.value = swUpdateServiceWorker;
  });

  const closePrompt = () => {
    needRefresh.value = false;
  };

  const updateApp = async () => {
    if (updateServiceWorker.value) {
      await updateServiceWorker.value();
      // Reload the page to load new content
      window.location.reload();
    }
  };

  return {
    needRefresh,
    updateApp,
    closePrompt,
  };
}
