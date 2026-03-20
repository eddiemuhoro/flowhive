<template>
  <AppBootstrapShell v-if="appStore.bootstrapping" />
  <RouterView v-else />
  <PWAInstallPrompt v-if="!appStore.bootstrapping" />
  <PWAUpdatePrompt v-if="!appStore.bootstrapping" />
  <PushNotificationPrompt v-if="!appStore.bootstrapping" />
</template>

<script setup lang="ts">
import AppBootstrapShell from "@/components/AppBootstrapShell.vue";
import PWAInstallPrompt from "@/components/PWAInstallPrompt.vue";
import PWAUpdatePrompt from "@/components/PWAUpdatePrompt.vue";
import PushNotificationPrompt from "@/components/PushNotificationPrompt.vue";
import { useAppStore } from "@/stores/app";

const appStore = useAppStore();
</script>
