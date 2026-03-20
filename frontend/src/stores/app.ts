import { defineStore } from "pinia";
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useWorkspaceStore } from "@/stores/workspace";

export const useAppStore = defineStore("app", () => {
  const bootstrapping = ref(true);
  const bootstrapped = ref(false);
  let bootstrapPromise: Promise<void> | null = null;

  const bootstrap = async () => {
    if (bootstrapped.value) return;
    if (bootstrapPromise) return bootstrapPromise;

    bootstrapping.value = true;
    bootstrapPromise = (async () => {
      const authStore = useAuthStore();
      const workspaceStore = useWorkspaceStore();

      await authStore.initialize();
      if (authStore.isAuthenticated) {
        await workspaceStore.initializeWorkspace();
      }
      bootstrapped.value = true;
    })();

    try {
      await bootstrapPromise;
    } finally {
      bootstrapping.value = false;
    }
  };

  return {
    bootstrapping,
    bootstrapped,
    bootstrap,
  };
});
