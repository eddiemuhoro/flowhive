import { ref, onMounted } from 'vue';
import { useRegisterSW } from 'virtual:pwa-register/vue';

export function usePWA() {
  const needRefresh = ref(false);
  const offlineReady = ref(false);
  const updateServiceWorker = ref<(() => Promise<void>) | undefined>();

  const {
    needRefresh: swNeedRefresh,
    offlineReady: swOfflineReady,
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
    onOfflineReady() {
      offlineReady.value = true;
    },
  });

  // Sync refs
  onMounted(() => {
    needRefresh.value = swNeedRefresh.value;
    offlineReady.value = swOfflineReady.value;
    updateServiceWorker.value = swUpdateServiceWorker;
  });

  const closePrompt = () => {
    needRefresh.value = false;
    offlineReady.value = false;
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
    offlineReady,
    updateApp,
    closePrompt,
  };
}
