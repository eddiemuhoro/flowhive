<!-- Workspace Switcher Component -->
<!-- Allows users to quickly switch between their workspaces -->

<template>
  <div class="relative" ref="dropdownRef">
    <button
      @click="isOpen = !isOpen"
      class="flex w-full items-center justify-between rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm hover:bg-gray-50"
    >
      <div class="flex items-center space-x-2 truncate">
        <div
          v-if="currentWorkspace"
          class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded text-sm font-bold text-white"
          :style="{ backgroundColor: currentWorkspace.color || '#0ea5e9' }"
        >
          {{
            currentWorkspace.icon ||
            currentWorkspace.name.charAt(0).toUpperCase()
          }}
        </div>
        <span class="truncate font-medium text-gray-900">
          {{ currentWorkspace?.name || "Select Workspace" }}
        </span>
      </div>
      <svg
        class="h-5 w-5 flex-shrink-0 text-gray-400"
        :class="{ 'rotate-180': isOpen }"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M19 9l-7 7-7-7"
        />
      </svg>
    </button>

    <!-- Dropdown -->
    <div
      v-if="isOpen"
      class="absolute left-0 right-0 z-50 mt-2 max-h-80 overflow-y-auto rounded-lg border border-gray-200 bg-white shadow-lg"
    >
      <div class="p-2">
        <div
          v-for="workspace in workspaces"
          :key="workspace.id"
          @click="switchWorkspace(workspace)"
          class="flex cursor-pointer items-center space-x-3 rounded-lg px-3 py-2 hover:bg-gray-100"
          :class="{
            'bg-blue-50': currentWorkspace?.id === workspace.id,
          }"
        >
          <div
            class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded text-sm font-bold text-white"
            :style="{ backgroundColor: workspace.color || '#0ea5e9' }"
          >
            {{ workspace.icon || workspace.name.charAt(0).toUpperCase() }}
          </div>
          <div class="flex-1 truncate">
            <p class="truncate text-sm font-medium text-gray-900">
              {{ workspace.name }}
            </p>
            <p class="truncate text-xs text-gray-500">
              {{
                workspace.workspace_type === "FIELD_OPERATIONS"
                  ? "Field Operations"
                  : "Project Management"
              }}
            </p>
          </div>
          <svg
            v-if="currentWorkspace?.id === workspace.id"
            class="h-5 w-5 flex-shrink-0 text-blue-600"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
              clip-rule="evenodd"
            />
          </svg>
        </div>
      </div>

      <!-- Create New Workspace -->
      <div class="border-t border-gray-200 p-2">
        <button
          @click="goToWorkspaces"
          class="flex w-full items-center space-x-2 rounded-lg px-3 py-2 text-sm font-medium text-blue-600 hover:bg-blue-50"
        >
          <svg
            class="h-5 w-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 4v16m8-8H4"
            />
          </svg>
          <span>View All Workspaces</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useWorkspaceStore } from "@/stores/workspace";
import type { Workspace } from "@/types/workspace";

const router = useRouter();
const workspaceStore = useWorkspaceStore();

const isOpen = ref(false);
const dropdownRef = ref<HTMLElement | null>(null);

const workspaces = computed(() => workspaceStore.workspaces);
const currentWorkspace = computed(() => workspaceStore.currentWorkspace);

const switchWorkspace = async (workspace: Workspace) => {
  isOpen.value = false;
  await workspaceStore.fetchWorkspace(workspace.id);

  // Route based on workspace type
  if (workspace.workspace_type === "FIELD_OPERATIONS") {
    router.push("/field");
  } else {
    router.push(`/workspace/${workspace.id}`);
  }
};

const goToWorkspaces = () => {
  isOpen.value = false;
  router.push("/workspaces");
};

// Close dropdown when clicking outside
const handleClickOutside = (event: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
  // Load workspaces if not already loaded
  if (workspaces.value.length === 0) {
    workspaceStore.fetchWorkspaces();
  }
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>
