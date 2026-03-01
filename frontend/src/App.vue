<template>
  <RouterView />
  <PWAInstallPrompt />
  <PWAUpdatePrompt />
  <PushNotificationPrompt />
</template>

<script setup lang="ts">
import PWAInstallPrompt from "@/components/PWAInstallPrompt.vue";
import PWAUpdatePrompt from "@/components/PWAUpdatePrompt.vue";
import PushNotificationPrompt from "@/components/PushNotificationPrompt.vue";
// Auth is initialized in main.ts and router, no need to initialize here
</script>
