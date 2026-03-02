<template>
  <div v-if="showPrompt" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 p-4">
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
      <div class="flex items-start mb-4">
        <div class="flex-shrink-0">
          <svg class="h-12 w-12 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
        </div>
        <div class="ml-4 flex-1">
          <h3 class="text-lg font-semibold text-gray-900 mb-2">
            Enable Notifications
          </h3>
          <p class="text-sm text-gray-600 mb-4">
            Flowhive needs notification access to keep you updated on:
          </p>
          <ul class="text-sm text-gray-600 space-y-1 mb-4">
            <li class="flex items-center">
              <svg class="h-4 w-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              Weekly report notifications
            </li>
            <li class="flex items-center">
              <svg class="h-4 w-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              Task assignments and updates
            </li>
            <li class="flex items-center">
              <svg class="h-4 w-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              Team collaboration alerts
            </li>
          </ul>

          <div v-if="error" class="mb-4 p-3 bg-red-50 rounded-md">
            <p class="text-sm text-red-600">{{ error }}</p>
          </div>
        </div>
      </div>

      <div class="flex gap-3">
        <button
          @click="enableNotifications"
          :disabled="loading"
          class="flex-1 bg-indigo-600 text-white py-2.5 px-4 rounded-lg font-medium hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="!loading">Enable Notifications</span>
          <span v-else>Enabling...</span>
        </button>
        <button
          @click="dismiss"
          :disabled="loading"
          class="px-4 py-2.5 text-gray-600 hover:text-gray-800 font-medium transition-colors"
        >
          Later
        </button>
      </div>

      <p class="text-xs text-gray-500 mt-3 text-center">
        You can change this later in your browser settings
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { pushService } from '@/services/push.service'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const showPrompt = ref(false)
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  // Check if we should show the prompt
  await checkShouldShow()
})

// Watch for authentication changes
watch(() => authStore.isAuthenticated, async (isAuthenticated) => {
  if (isAuthenticated) {
    // User just logged in - check if we should show prompt
    await checkShouldShow()
  } else {
    // User logged out - hide prompt
    showPrompt.value = false
  }
})

async function checkShouldShow() {
  // Don't show if user is not authenticated
  if (!authStore.isAuthenticated) {
    return
  }

  // Don't show if notifications not supported
  if (!pushService.isSupported()) {
    return
  }

  // Don't show if already subscribed
  const isSubscribed = await pushService.isSubscribed()
  if (isSubscribed) {
    return
  }

  // Check permission status
  const permission = pushService.getPermissionStatus()

  // Don't show if user explicitly denied permission
  if (permission === 'denied') {
    return
  }

  // Don't show if user previously dismissed (check localStorage)
  // const dismissed = localStorage.getItem('push-notification-dismissed')
  // if (dismissed) {
  //   const expiryDate = new Date(dismissed)
  //   // Check if dismissal has expired
  //   if (expiryDate > new Date()) {
  //     return
  //   }
  // }

  // Show prompt if:
  // 1. Permission is 'default' (not yet asked), OR
  // 2. Permission is 'granted' but user is not subscribed
  //    (e.g., they granted permission before feature was implemented)
  if (permission === 'default' || (permission === 'granted' && !isSubscribed)) {
    showPrompt.value = true
  }
}

async function enableNotifications() {
  loading.value = true
  error.value = ''

  try {
    await pushService.subscribe()
    showPrompt.value = false
    // Clear any previous dismissal since user successfully subscribed
    localStorage.removeItem('push-notification-dismissed')

    // Show success message (optional)
    console.log('Push notifications enabled successfully')

  } catch (err: any) {
    error.value = err.message || 'Failed to enable notifications. Please try again.'
    console.error('Failed to enable push notifications:', err)
  } finally {
    loading.value = false
  }
}

function dismiss() {
  showPrompt.value = false
  // Only remember dismissal if user is authenticated
  if (authStore.isAuthenticated) {
    // Remember dismissal for 7 days
    const expiryDate = new Date()
    expiryDate.setDate(expiryDate.getDate() + 7)
    localStorage.setItem('push-notification-dismissed', expiryDate.toISOString())
  }
  // If not authenticated, don't save dismissal so prompt shows again after login
}
</script>
