<!-- Field Settings View -->
<!-- Manager settings for task categories and field operations configuration -->

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <div class="mx-auto max-w-4xl space-y-6">
      <!-- Header -->
      <div>
        <h1 class="text-2xl font-bold text-gray-900">
          Field Operations Settings
        </h1>
        <p class="mt-1 text-sm text-gray-600">
          Manage task categories and field operations configuration
        </p>
      </div>

      <!-- Task Categories Section -->
      <TaskCategoriesSection :workspace-id="currentWorkspaceId" />

  <!-- User Management Section (Executive Only) -->
      <UserManagementSection
        :workspace="currentWorkspace"
        :current-user-id="currentUser?.id"
        :current-user-role="currentUser?.role"
      />

      <!-- Permission Settings Section -->
      <PermissionSettingsSection />

      <!-- Workspace Settings Section -->
      <WorkspaceSettingsSection
        :workspace="currentWorkspace"
        :current-user-id="currentUser?.id"
        :current-user-role="currentUser?.role"
      />


    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useWorkspaceStore } from "@/stores/workspace";
import { useAuthStore } from "@/stores/auth";
import TaskCategoriesSection from "./components/settings/TaskCategoriesSection.vue";
import PermissionSettingsSection from "./components/settings/PermissionSettingsSection.vue";
import WorkspaceSettingsSection from "./components/settings/WorkspaceSettingsSection.vue";
import UserManagementSection from "./components/settings/UserManagementSection.vue";

const workspaceStore = useWorkspaceStore();
const authStore = useAuthStore();

const currentUser = computed(() => authStore.user);
const currentWorkspace = computed(() => workspaceStore.currentWorkspace);
const currentWorkspaceId = computed(() => currentWorkspace.value?.id || 0);
</script>
