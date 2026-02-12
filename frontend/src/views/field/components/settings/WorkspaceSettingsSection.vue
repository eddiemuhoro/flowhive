<!-- Workspace Settings Section Component -->
<template>
  <div class="rounded-lg bg-white p-6 shadow-sm">
    <h2 class="text-lg font-semibold text-gray-900 mb-4">
      Workspace Settings
    </h2>

    <div class="space-y-6">
      <!-- Workspace Info -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Workspace Name
        </label>
        <div class="flex items-center space-x-2">
          <input
            v-model="workspaceName"
            type="text"
            :disabled="!isOwnerOrExecutive"
            class="flex-1 rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none disabled:bg-gray-100 disabled:text-gray-500"
          />
          <button
            v-if="isOwnerOrExecutive && workspaceName !== workspace?.name"
            @click="handleUpdateWorkspace"
            :disabled="loading"
            class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {{ loading ? "Saving..." : "Save" }}
          </button>
        </div>
      </div>

      <!-- Danger Zone (Executive/Owner Only) -->
      <!-- <div v-if="isOwnerOrExecutive" class="rounded-lg border border-red-200 bg-red-50 p-4">
        <h3 class="text-sm font-semibold text-red-900 mb-3">
          Danger Zone
        </h3>
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-red-900">Delete Workspace</p>
              <p class="text-xs text-red-700">Permanently delete this workspace and all its data</p>
            </div>
            <button
              @click="handleDeleteWorkspace"
              class="rounded-lg border border-red-300 bg-white px-4 py-2 text-sm font-medium text-red-700 hover:bg-red-50"
            >
              Delete
            </button>
          </div>
        </div>
      </div> -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useWorkspaceStore } from "@/stores/workspace";
import type { WorkspaceDetail } from "@/types/workspace";

interface Props {
  workspace: WorkspaceDetail | null;
  currentUserRole: string | undefined;
  currentUserId: number | undefined;
}

const props = defineProps<Props>();

const workspaceStore = useWorkspaceStore();

const workspaceName = ref("");
const loading = ref(false);

const isOwnerOrExecutive = computed(() => {
  const isOwner = props.workspace?.owner_id === props.currentUserId;
  const isExecutive = props.currentUserRole === "executive";
  return isOwner || isExecutive;
});

// Initialize workspace name when workspace changes
watch(
  () => props.workspace?.name,
  (newName) => {
    if (newName) {
      workspaceName.value = newName;
    }
  },
  { immediate: true }
);

const handleUpdateWorkspace = async () => {
  if (!props.workspace?.id || !workspaceName.value.trim()) return;

  loading.value = true;
  try {
    await workspaceStore.updateWorkspace(props.workspace.id, {
      name: workspaceName.value,
    });
    alert("Workspace updated successfully!");
  } catch (error: any) {
    console.error("Failed to update workspace:", error);
    alert(
      error.response?.data?.detail ||
        "Failed to update workspace. Please try again.",
    );
    // Reset to original name on error
    workspaceName.value = props.workspace?.name || "";
  } finally {
    loading.value = false;
  }
};

const handleDeleteWorkspace = async () => {
  const name = props.workspace?.name;

  if (
    !confirm(
      `Are you sure you want to delete "${name}"?\n\nThis action cannot be undone. All field activities, categories, and data will be permanently deleted.`
    )
  ) {
    return;
  }

  const confirmText = prompt(
    `To confirm deletion, please type the workspace name: "${name}"`
  );

  if (confirmText !== name) {
    alert("Workspace name doesn't match. Deletion cancelled.");
    return;
  }

  if (!props.workspace?.id) return;

  try {
    await workspaceStore.deleteWorkspace(props.workspace.id);
    alert("Workspace deleted successfully");
  } catch (error: any) {
    console.error("Failed to delete workspace:", error);
    alert(
      error.response?.data?.detail ||
        "Failed to delete workspace. Please try again.",
    );
  }
};
</script>
