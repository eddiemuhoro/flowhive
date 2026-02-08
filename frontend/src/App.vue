<template>
  <RouterView />
  <PWAInstallPrompt />
  <PWAUpdatePrompt />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import PWAInstallPrompt from '@/components/PWAInstallPrompt.vue'
import PWAUpdatePrompt from '@/components/PWAUpdatePrompt.vue'

const authStore = useAuthStore()

onMounted(async () => {
  await authStore.initialize()
})
</script>
