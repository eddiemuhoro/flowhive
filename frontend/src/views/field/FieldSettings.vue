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
      <div class="rounded-lg bg-white p-6 shadow-sm">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-900">Task Categories</h2>
          <button
            @click="showCategoryForm = true"
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
            <span>Add Category</span>
          </button>
        </div>

        <!-- Loading State -->
        <div
          v-if="categoryStore.loading"
          class="flex items-center justify-center py-8"
        >
          <div
            class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"
          ></div>
        </div>

        <!-- Categories List -->
        <div v-else-if="allCategories.length > 0" class="space-y-3">
          <div
            v-for="category in allCategories"
            :key="category.id"
            class="flex items-center justify-between rounded-lg border p-4"
            :class="
              category.is_active
                ? 'border-gray-200'
                : 'border-gray-200 bg-gray-50 opacity-60'
            "
          >
            <div class="flex items-center space-x-4">
              <!-- Color Preview -->
              <div
                class="h-10 w-10 rounded-lg"
                :style="{ backgroundColor: category.color }"
              ></div>

              <div>
                <div class="flex items-center space-x-2">
                  <p class="font-medium text-gray-900">{{ category.title }}</p>
                  <span
                    v-if="!category.is_active"
                    class="rounded-full bg-gray-200 px-2 py-0.5 text-xs font-medium text-gray-600"
                  >
                    Inactive
                  </span>
                </div>
                <p class="text-sm text-gray-500">{{ category.name }}</p>
                <p
                  v-if="category.description"
                  class="mt-1 text-sm text-gray-600"
                >
                  {{ category.description }}
                </p>
              </div>
            </div>

            <div class="flex items-center space-x-2">
              <button
                @click="editCategory(category)"
                class="rounded-lg p-2 text-gray-600 hover:bg-gray-100"
                title="Edit"
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
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                  />
                </svg>
              </button>
              <button
                v-if="category.is_active"
                @click="deactivateCategory(category)"
                class="rounded-lg p-2 text-orange-600 hover:bg-orange-50"
                title="Deactivate"
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
                    d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"
                  />
                </svg>
              </button>
              <button
                v-else
                @click="activateCategory(category)"
                class="rounded-lg p-2 text-green-600 hover:bg-green-50"
                title="Activate"
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
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="py-8 text-center">
          <p class="text-sm text-gray-500">
            No task categories yet. Create your first one!
          </p>
        </div>
      </div>

      <!-- Team Members Section -->
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
        <div v-if="currentWorkspace?.members" class="space-y-3">
          <div
            v-for="member in currentWorkspace.members"
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
                v-if="member.user_id === currentWorkspace.owner_id"
                class="rounded bg-blue-100 px-2 py-1 text-xs font-medium text-blue-700"
              >
                Owner
              </span>
              <span
                v-else-if="member.role"
                class="rounded bg-gray-100 px-2 py-1 text-xs font-medium text-gray-700 capitalize"
              >
                {{ member.role }}
              </span>
              <button
                v-if="
                  canManageMembers &&
                  member.user_id !== currentWorkspace.owner_id &&
                  member.user_id !== currentUser?.id
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
      </div>

      <!-- Additional Settings (Future) -->
      <div class="rounded-lg bg-white p-6 shadow-sm">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">
          Additional Settings
        </h2>
        <p class="text-sm text-gray-500">
          More configuration options coming soon...
        </p>
      </div>
    </div>

    <!-- Category Form Modal -->
    <Teleport to="body">
      <div
        v-if="showCategoryForm"
        class="fixed inset-0 z-50 overflow-y-auto bg-black/50 p-4"
        @click.self="closeCategoryForm"
      >
        <div class="mx-auto max-w-lg rounded-lg bg-white p-6 shadow-xl">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-semibold text-gray-900">
              {{ editingCategory ? "Edit Category" : "New Task Category" }}
            </h2>
            <button
              @click="closeCategoryForm"
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

          <form @submit.prevent="handleCategorySubmit" class="space-y-4">
            <!-- Title -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Display Title <span class="text-red-500">*</span>
              </label>
              <input
                v-model="categoryForm.title"
                @input="autoGenerateSlug"
                type="text"
                required
                placeholder="e.g., Installation, Maintenance"
                class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
              />
            </div>

            <!-- Name (Slug) - Auto-generated -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Name (slug) <span class="text-red-500">*</span>
              </label>
              <input
                v-model="categoryForm.name"
                type="text"
                required
                placeholder="e.g., installation, maintenance"
                class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
              />
              <p class="mt-1 text-xs text-gray-500">
                Auto-generated from title (you can edit if needed)
              </p>
            </div>

            <!-- Description -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1"
                >Description</label
              >
              <textarea
                v-model="categoryForm.description"
                rows="2"
                placeholder="Brief description of this category"
                class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
              ></textarea>
            </div>

            <!-- Color -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Color <span class="text-red-500">*</span>
              </label>
              <div class="flex items-center space-x-3">
                <input
                  v-model="categoryForm.color"
                  type="color"
                  required
                  class="h-10 w-20 rounded cursor-pointer"
                />
                <input
                  v-model="categoryForm.color"
                  type="text"
                  required
                  placeholder="#3B82F6"
                  class="flex-1 rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
                />
              </div>
            </div>

            <!-- Icon (Emoji) -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1"
                >Icon (Emoji)</label
              >
              <input
                v-model="categoryForm.icon"
                type="text"
                maxlength="2"
                placeholder="🔧"
                class="w-full rounded-lg border border-gray-300 px-3 py-2 text-2xl focus:border-blue-500 focus:outline-none"
              />
            </div>

            <!-- Actions -->
            <div class="flex items-center justify-end space-x-3 border-t pt-4">
              <button
                type="button"
                @click="closeCategoryForm"
                class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="formLoading"
                class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
              >
                {{
                  formLoading
                    ? "Saving..."
                    : editingCategory
                      ? "Update"
                      : "Create"
                }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

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
import { ref, computed, onMounted } from "vue";
import { useWorkspaceStore } from "@/stores/workspace";
import { useTaskCategoryStore } from "@/stores/taskCategory";
import { useAuthStore } from "@/stores/auth";
import type {
  TaskCategory,
  TaskCategoryCreate,
  TaskCategoryUpdate,
} from "@/types/field";

const workspaceStore = useWorkspaceStore();
const categoryStore = useTaskCategoryStore();
const authStore = useAuthStore();

const currentUser = computed(() => authStore.user);
const currentWorkspace = computed(() => workspaceStore.currentWorkspace);
const currentWorkspaceId = computed(() => currentWorkspace.value?.id || 0);

const showCategoryForm = ref(false);
const editingCategory = ref<TaskCategory | null>(null);
const formLoading = ref(false);

// Member management
const showAddMember = ref(false);
const searchQuery = ref("");
const searchResults = ref<any[]>([]);
const searching = ref(false);
let searchTimeout: NodeJS.Timeout | null = null;

const categoryForm = ref<TaskCategoryCreate>({
  name: "",
  title: "",
  description: "",
  color: "#3B82F6",
  icon: "",
  workspace_id: 0,
});

const allCategories = computed(() => {
  return [...categoryStore.categories].sort((a, b) => {
    // Active first, then by name
    if (a.is_active !== b.is_active) {
      return a.is_active ? -1 : 1;
    }
    return a.name.localeCompare(b.name);
  });
});

const canManageMembers = computed(() => {
  const role = currentUser.value?.role?.toUpperCase();
  const isOwner = currentWorkspace.value?.owner_id === currentUser.value?.id;
  return role === "MANAGER" || role === "EXECUTIVE" || isOwner;
});

// const isOwner = computed(() => {
//   return currentWorkspace.value?.owner_id === currentUser.value?.id;
// });

const loadCategories = async () => {
  if (!currentWorkspaceId.value) return;

  try {
    await categoryStore.fetchCategories(currentWorkspaceId.value, true); // Include inactive
  } catch (error) {
    console.error("Failed to load categories:", error);
  }
};

const editCategory = (category: TaskCategory) => {
  editingCategory.value = category;
  categoryForm.value = {
    name: category.name,
    title: category.title,
    description: category.description || "",
    color: category.color,
    icon: category.icon || "",
    workspace_id: currentWorkspaceId.value,
  };
  showCategoryForm.value = true;
};

const handleCategorySubmit = async () => {
  categoryForm.value.workspace_id = currentWorkspaceId.value;
  formLoading.value = true;

  try {
    if (editingCategory.value) {
      const updateData: TaskCategoryUpdate = {
        name: categoryForm.value.name,
        title: categoryForm.value.title,
        description: categoryForm.value.description || undefined,
        color: categoryForm.value.color,
        icon: categoryForm.value.icon || undefined,
      };
      await categoryStore.updateCategory(editingCategory.value.id, updateData);
    } else {
      await categoryStore.createCategory(categoryForm.value);
    }
    closeCategoryForm();
    await loadCategories();
  } catch (error: any) {
    console.error("Failed to save category:", error);
    alert(
      error.response?.data?.detail ||
        "Failed to save category. Please try again.",
    );
  } finally {
    formLoading.value = false;
  }
};

const deactivateCategory = async (category: TaskCategory) => {
  if (
    !confirm(
      `Deactivate "${category.title}"? It will be hidden from activity forms but existing activities will retain this category.`,
    )
  ) {
    return;
  }

  try {
    await categoryStore.deleteCategory(category.id);
    await loadCategories();
  } catch (error: any) {
    console.error("Failed to deactivate category:", error);
    alert(
      error.response?.data?.detail ||
        "Failed to deactivate category. Please try again.",
    );
  }
};

const activateCategory = async (category: TaskCategory) => {
  try {
    await categoryStore.updateCategory(category.id, {
      is_active: true,
    });
    await loadCategories();
  } catch (error: any) {
    console.error("Failed to activate category:", error);
    alert(
      error.response?.data?.detail ||
        "Failed to activate category. Please try again.",
    );
  }
};

const autoGenerateSlug = () => {
  // Only auto-generate if not editing an existing category
  if (!editingCategory.value && categoryForm.value.title) {
    categoryForm.value.name = categoryForm.value.title
      .toLowerCase()
      .replace(/\s+/g, '_')
      .replace(/[^a-z0-9_]/g, '');
  }
};

const closeCategoryForm = () => {
  showCategoryForm.value = false;
  editingCategory.value = null;
  categoryForm.value = {
    name: "",
    title: "",
    description: "",
    color: "#3B82F6",
    icon: "",
    workspace_id: 0,
  };
};

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
      // Filter out users who are already members
      const memberIds =
        currentWorkspace.value?.members.map((m) => m.user_id) || [];
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
  if (!currentWorkspaceId.value) return;

  try {
    await workspaceStore.addMember(currentWorkspaceId.value, userId);
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

  if (!currentWorkspaceId.value) return;

  try {
    await workspaceStore.removeMember(currentWorkspaceId.value, userId);
  } catch (error: any) {
    console.error("Failed to remove member:", error);
    alert(
      error.response?.data?.detail ||
        "Failed to remove member. Please try again.",
    );
  }
};

onMounted(() => {
  loadCategories();
});
</script>
