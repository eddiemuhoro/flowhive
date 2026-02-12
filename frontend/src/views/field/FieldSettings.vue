<!-- Field Settings View -->
<!-- Manager settings for task categories and field operations configuration -->

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <div class="mx-auto max-w-4xl">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-gray-900">
          Field Operations Settings
        </h1>
        <p class="mt-1 text-sm text-gray-600">
          Manage task categories and field operations configuration
        </p>
      </div>

      <!-- Tabs Navigation -->
      <div class="mb-6 border-b border-gray-200">
        <nav class="-mb-px flex space-x-8" aria-label="Tabs">
          <button
            @click="activeTab = 'categories'"
            :class="[
              activeTab === 'categories'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
              'whitespace-nowrap border-b-2 px-1 py-4 text-sm font-medium'
            ]"
          >
            Task Categories
          </button>
          <button
            v-if="currentUser?.role === 'executive'"
            @click="activeTab = 'users'"
            :class="[
              activeTab === 'users'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
              'whitespace-nowrap border-b-2 px-1 py-4 text-sm font-medium'
            ]"
          >
            User Management
          </button>
          <button
            @click="activeTab = 'permissions'"
            :class="[
              activeTab === 'permissions'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
              'whitespace-nowrap border-b-2 px-1 py-4 text-sm font-medium'
            ]"
          >
            Permissions
          </button>
          <button
            @click="activeTab = 'workspace'"
            :class="[
              activeTab === 'workspace'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
              'whitespace-nowrap border-b-2 px-1 py-4 text-sm font-medium'
            ]"
          >
            Workspace
          </button>
        </nav>
      </div>

      <!-- Tab Content -->
      <div class="mt-6">
        <!-- Task Categories Tab -->
        <TaskCategoriesSection
          v-if="activeTab === 'categories'"
          :workspace-id="currentWorkspaceId"
        />

        <!-- User Management Tab (Executive Only) -->
        <UserManagementSection
          v-if="activeTab === 'users' && currentUser?.role === 'executive'"
          :workspace="currentWorkspace"
          :current-user-id="currentUser?.id"
          :current-user-role="currentUser?.role"
        />

        <!-- Permission Settings Tab -->
        <PermissionSettingsSection v-if="activeTab === 'permissions'" />

        <!-- Workspace Settings Tab -->
        <WorkspaceSettingsSection
          v-if="activeTab === 'workspace'"
          :workspace="currentWorkspace"
          :current-user-id="currentUser?.id"
          :current-user-role="currentUser?.role"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useWorkspaceStore } from "@/stores/workspace";
import { useAuthStore } from "@/stores/auth";
import TaskCategoriesSection from "./components/settings/TaskCategoriesSection.vue";
import PermissionSettingsSection from "./components/settings/PermissionSettingsSection.vue";
import WorkspaceSettingsSection from "./components/settings/WorkspaceSettingsSection.vue";
import UserManagementSection from "./components/settings/UserManagementSection.vue";

const workspaceStore = useWorkspaceStore();
const authStore = useAuthStore();

const activeTab = ref('categories');
const currentUser = computed(() => authStore.user);
const currentWorkspace = computed(() => workspaceStore.currentWorkspace);
const currentWorkspaceId = computed(() => currentWorkspace.value?.id || 0);
</script>
