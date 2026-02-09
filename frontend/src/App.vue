<template>
  <RouterView />
  <PWAInstallPrompt />
  <PWAUpdatePrompt />
</template>

<script setup lang="ts">
import PWAInstallPrompt from "@/components/PWAInstallPrompt.vue";
import PWAUpdatePrompt from "@/components/PWAUpdatePrompt.vue";
// Auth is initialized in main.ts and router, no need to initialize here
</script>
