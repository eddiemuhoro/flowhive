<script setup lang="ts">
import { ref, onMounted } from 'vue';

// PWA install prompt interface
interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

const showInstallPrompt = ref(false);
const deferredPrompt = ref<BeforeInstallPromptEvent | null>(null);
const isInstalled = ref(false);

onMounted(() => {
  // Check if app is already installed
  if (window.matchMedia('(display-mode: standalone)').matches) {
    isInstalled.value = true;
    return;
  }

  // Listen for the beforeinstallprompt event
  window.addEventListener('beforeinstallprompt', (e: Event) => {
    // Prevent the mini-infobar from appearing on mobile
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt.value = e as BeforeInstallPromptEvent;
    // Show the install button
    showInstallPrompt.value = true;
  });

  // Listen for successful installation
  window.addEventListener('appinstalled', () => {
    deferredPrompt.value = null;
    showInstallPrompt.value = false;
    isInstalled.value = true;
  });
});

const installApp = async () => {
  if (!deferredPrompt.value) return;

  // Show the install prompt
  deferredPrompt.value.prompt();

  // Wait for the user to respond to the prompt
  const { outcome } = await deferredPrompt.value.userChoice;

  if (outcome === 'accepted') {
    console.log('User accepted the install prompt');
  }

  // Clear the deferred prompt
  deferredPrompt.value = null;
  showInstallPrompt.value = false;
};

const dismissPrompt = () => {
  showInstallPrompt.value = false;
  // Store dismissal in localStorage to not show again for a while
  localStorage.setItem('pwa-install-dismissed', Date.now().toString());
};

// Check if user dismissed recently (within 7 days)
const checkDismissalStatus = () => {
  const dismissedTime = localStorage.getItem('pwa-install-dismissed');
  if (dismissedTime) {
    const sevenDaysInMs = 7 * 24 * 60 * 60 * 1000;
    const timeSinceDismissal = Date.now() - parseInt(dismissedTime);
    if (timeSinceDismissal < sevenDaysInMs) {
      showInstallPrompt.value = false;
    }
  }
};

onMounted(() => {
  checkDismissalStatus();
});
</script>

<template>
  <transition
    enter-active-class="transition ease-out duration-300"
    enter-from-class="opacity-0 translate-y-4"
    enter-to-class="opacity-100 translate-y-0"
    leave-active-class="transition ease-in duration-200"
    leave-from-class="opacity-100 translate-y-0"
    leave-to-class="opacity-0 translate-y-4"
  >
    <div
      v-if="showInstallPrompt && !isInstalled"
      class="fixed bottom-4 left-4 right-4 md:left-auto md:right-4 md:max-w-sm z-50"
    >
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-4">
        <div class="flex items-start gap-3">
          <div class="flex-shrink-0">
            <img src="/favicon.svg" alt="Flowhive" class="w-10 h-10 rounded-lg" />
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-sm font-semibold text-gray-900 dark:text-gray-100">
              Install Flowhive
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Install our app for a faster, native-like experience
            </p>
            <div class="flex gap-2 mt-3">
              <button
                @click="installApp"
                class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-colors"
              >
                Install
              </button>
              <button
                @click="dismissPrompt"
                class="px-4 py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 text-sm font-medium rounded-lg transition-colors"
              >
                Not now
              </button>
            </div>
          </div>
          <button
            @click="dismissPrompt"
            class="flex-shrink-0 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>
