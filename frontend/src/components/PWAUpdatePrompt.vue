<script setup lang="ts">
import { usePWA } from '@/composables/usePWA';

const { needRefresh, offlineReady, updateApp, closePrompt } = usePWA();
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
      v-if="needRefresh || offlineReady"
      class="fixed bottom-4 left-4 right-4 md:left-auto md:right-4 md:max-w-sm z-50"
    >
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-4">
        <div class="flex items-start gap-3">
          <div class="flex-shrink-0">
            <svg
              v-if="needRefresh"
              class="w-6 h-6 text-indigo-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
            <svg
              v-else
              class="w-6 h-6 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-sm font-semibold text-gray-900 dark:text-gray-100">
              {{ needRefresh ? 'Update Available' : 'Ready for Offline Use' }}
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
              {{
                needRefresh
                  ? 'A new version is available. Reload to update.'
                  : 'The app is ready to work offline.'
              }}
            </p>
            <div class="flex gap-2 mt-3">
              <button
                v-if="needRefresh"
                @click="updateApp"
                class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-colors"
              >
                Reload
              </button>
              <button
                @click="closePrompt"
                class="px-4 py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 text-sm font-medium rounded-lg transition-colors"
              >
                {{ needRefresh ? 'Later' : 'Close' }}
              </button>
            </div>
          </div>
          <button
            @click="closePrompt"
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
