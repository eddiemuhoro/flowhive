<!-- Team Members Section Component -->
<template>
  <div class="rounded-lg bg-white p-6 shadow-sm">
    <div class="mb-4 flex items-center justify-between">
      <h2 class="text-lg font-semibold text-gray-900">Team Members</h2>
      <button
        v-if="canManageMembers"
        @click="showAddMember = true"
        class="flex items-center space-x-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
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
        <span>Add Member</span>
      </button>
    </div>

    <!-- Members List -->
    <div v-if="workspace?.members" class="space-y-3">
      <div
        v-for="member in workspace.members"
        :key="member.user_id"
        class="flex items-center justify-between rounded-lg border border-gray-200 p-4 hover:bg-gray-50"
      >
        <div class="flex items-center space-x-3">
          <div
            class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-blue-500 text-sm font-semibold text-white"
          >
            {{
              (member.full_name || member.username).charAt(0).toUpperCase()
            }}
          </div>
          <div>
            <p class="text-sm font-medium text-gray-900">
              {{ member.full_name || member.username }}
            </p>
            <p class="text-xs text-gray-500">{{ member.email }}</p>
          </div>
        </div>
        <div class="flex items-center space-x-2">
          <span
            v-if="member.user_id === workspace.owner_id"
            class="rounded bg-blue-100 px-2 py-1 text-xs font-medium text-blue-700"
          >
            Owner
          </span>
          <span
            v-if="member.system_role"
            :class="{
              'bg-purple-100 text-purple-700': member.system_role === 'executive',
              'bg-green-100 text-green-700': member.system_role === 'manager',
              'bg-gray-100 text-gray-700': member.system_role === 'team_member'
            }"
            class="rounded px-2 py-1 text-xs font-medium capitalize"
          >
            {{ member.system_role.replace('_', ' ') }}
          </span>
          <button
            v-if="
              canManageMembers &&
              member.user_id !== workspace.owner_id &&
              member.user_id !== currentUserId
            "
            @click="handleRemoveMember(member.user_id)"
            class="text-sm font-medium text-red-600 hover:text-red-800"
          >
            Remove
          </button>
        </div>
      </div>
    </div>

    <div v-else class="py-8 text-center text-sm text-gray-500">
      No members yet.
    </div>

    <!-- Add Member Modal -->
    <Teleport to="body">
      <div
        v-if="showAddMember"
        class="fixed inset-0 z-50 overflow-y-auto bg-black/50 p-4"
        @click.self="showAddMember = false"
      >
        <div class="mx-auto max-w-lg rounded-lg bg-white p-6 shadow-xl">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-semibold text-gray-900">Add Team Member</h2>
            <button
              @click="showAddMember = false"
              class="rounded-lg p-2 text-gray-400 hover:bg-gray-100"
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
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          <div class="space-y-4">
            <div>
              <label
                for="userSearch"
                class="mb-2 block text-sm font-medium text-gray-700"
              >
                Search by email or username
              </label>
              <input
                id="userSearch"
                v-model="searchQuery"
                @input="handleSearchUsers"
                type="text"
                placeholder="Type to search..."
                class="block w-full rounded-lg border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none sm:text-sm"
              />
            </div>

            <!-- Search Results -->
            <div
              v-if="searchResults.length > 0"
              class="max-h-60 overflow-y-auto rounded-lg border border-gray-200"
            >
              <button
                v-for="user in searchResults"
                :key="user.id"
                @click="handleAddMember(user.id)"
                class="w-full border-b border-gray-100 px-4 py-3 text-left hover:bg-gray-50 last:border-b-0"
              >
                <p class="text-sm font-medium text-gray-900">
                  {{ user.full_name || user.username }}
                </p>
                <p class="text-xs text-gray-500">{{ user.email }}</p>
              </button>
            </div>

            <div
              v-else-if="searchQuery && !searching"
              class="py-4 text-center text-sm text-gray-500"
            >
              No users found
            </div>

            <div
              v-if="searching"
              class="py-4 text-center text-sm text-gray-500"
            >
              Searching...
            </div>
          </div>

          <div class="mt-5 flex justify-end">
            <button
              @click="showAddMember = false"
              class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useWorkspaceStore } from "@/stores/workspace";
import type { WorkspaceDetail } from "@/types/workspace";

interface Props {
  workspace: WorkspaceDetail | null;
  currentUserId: number | undefined;
  currentUserRole: string | undefined;
}

const props = defineProps<Props>();

const workspaceStore = useWorkspaceStore();

const showAddMember = ref(false);
const searchQuery = ref("");
const searchResults = ref<any[]>([]);
const searching = ref(false);
let searchTimeout: NodeJS.Timeout | null = null;

const canManageMembers = computed(() => {
  const isOwner = props.workspace?.owner_id === props.currentUserId;
  const isExecutive = props.currentUserRole === "executive";
  const isManager = props.currentUserRole === "manager";
  return isOwner || isExecutive || isManager;
});

const handleSearchUsers = async () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout);
  }

  if (!searchQuery.value || searchQuery.value.length < 2) {
    searchResults.value = [];
    return;
  }

  searchTimeout = setTimeout(async () => {
    try {
      searching.value = true;
      const results = await workspaceStore.searchUsers(searchQuery.value);
      const memberIds = props.workspace?.members.map((m) => m.user_id) || [];
      searchResults.value = results.filter(
        (user) => !memberIds.includes(user.id),
      );
    } catch (error) {
      console.error("Failed to search users:", error);
    } finally {
      searching.value = false;
    }
  }, 300);
};

const handleAddMember = async (userId: number) => {
  if (!props.workspace?.id) return;

  try {
    await workspaceStore.addMember(props.workspace.id, userId);
    showAddMember.value = false;
    searchQuery.value = "";
    searchResults.value = [];
  } catch (error: any) {
    console.error("Failed to add member:", error);
    alert(
      error.response?.data?.detail || "Failed to add member. Please try again.",
    );
  }
};

const handleRemoveMember = async (userId: number) => {
  if (
    !confirm("Are you sure you want to remove this member from the workspace?")
  ) {
    return;
  }

  if (!props.workspace?.id) return;

  try {
    await workspaceStore.removeMember(props.workspace.id, userId);
  } catch (error: any) {
    console.error("Failed to remove member:", error);
    alert(
      error.response?.data?.detail ||
        "Failed to remove member. Please try again.",
    );
  }
};
</script>
