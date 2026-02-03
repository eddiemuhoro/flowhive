<!-- Field Activity Log View -->
<!-- Full activity log with filtering and search -->

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <div class="mx-auto max-w-7xl space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Activity Log</h1>
          <p class="mt-1 text-sm text-gray-600">
            {{ activityStore.activities.length }}
            {{
              activityStore.activities.length === 1 ? "activity" : "activities"
            }}
            logged
          </p>
        </div>
        <button
          @click="showActivityForm = true"
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
          <span>Log Activity</span>
        </button>
      </div>

      <!-- Activity List with Filters -->
      <ActivityList
        :activities="activityStore.activities"
        :workspace-id="currentWorkspaceId"
        :workspace-members="currentWorkspace?.members || []"
        :loading="activityStore.loading"
        @view="viewActivity"
        @edit="editActivity"
        @delete="deleteActivity"
        @filter="handleFilter"
      />

      <!-- Load More Button (if implementing pagination) -->
      <!-- <div v-if="hasMore" class="text-center">
        <button
          @click="loadMore"
          :disabled="activityStore.loading"
          class="rounded-lg border border-gray-300 px-6 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Load More Activities
        </button>
      </div> -->
    </div>

    <!-- Activity Form Modal -->
    <Teleport to="body">
      <div
        v-if="showActivityForm"
        class="fixed inset-0 z-50 overflow-y-auto bg-black/50 p-4"
        @click.self="closeActivityForm"
      >
        <div class="mx-auto max-w-2xl rounded-lg bg-white p-6 shadow-xl">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-semibold text-gray-900">
              {{ editingActivity ? "Edit Activity" : "Log New Activity" }}
            </h2>
            <button
              @click="closeActivityForm"
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
          <ActivityForm
            :workspace-id="currentWorkspaceId"
            :activity="editingActivity"
            :loading="formLoading"
            @submit="handleActivitySubmit"
            @cancel="closeActivityForm"
          />
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useWorkspaceStore } from "@/stores/workspace";
import { useFieldActivityStore } from "@/stores/fieldActivity";
import ActivityList from "@/components/field/activity/ActivityList.vue";
import ActivityForm from "@/components/field/activity/ActivityForm.vue";
import type {
  FieldActivityCreate,
  FieldActivityUpdate,
  FieldActivityFilters,
} from "@/types/field";

const router = useRouter();
const workspaceStore = useWorkspaceStore();
const activityStore = useFieldActivityStore();

const currentWorkspace = computed(() => workspaceStore.currentWorkspace);
const currentWorkspaceId = computed(() => currentWorkspace.value?.id || 0);

const showActivityForm = ref(false);
const editingActivity = ref<any>(null);
const formLoading = ref(false);

const loadActivities = async (filters?: FieldActivityFilters) => {
  if (!currentWorkspaceId.value) return;

  try {
    await activityStore.fetchActivities(currentWorkspaceId.value, filters);
  } catch (error) {
    console.error("Failed to load activities:", error);
  }
};

const handleFilter = async (filters: FieldActivityFilters) => {
  await loadActivities(filters);
};

const viewActivity = (activityId: number) => {
  router.push(`/field/activities/${activityId}`);
};

const editActivity = async (activityId: number) => {
  const activity = activityStore.activities.find((a) => a.id === activityId);
  if (activity) {
    editingActivity.value = activity;
    showActivityForm.value = true;
  }
};

const deleteActivity = async (activityId: number) => {
  if (
    !confirm(
      "Are you sure you want to delete this activity? This action cannot be undone.",
    )
  ) {
    return;
  }

  try {
    await activityStore.deleteActivity(activityId, currentWorkspaceId.value);
  } catch (error: any) {
    console.error("Failed to delete activity:", error);
    alert(
      error.response?.data?.detail ||
        "Failed to delete activity. Please try again.",
    );
  }
};

const handleActivitySubmit = async (
  data: FieldActivityCreate | FieldActivityUpdate,
) => {
  formLoading.value = true;
  try {
    if (editingActivity.value) {
      await activityStore.updateActivity(
        editingActivity.value.id,
        currentWorkspaceId.value,
        data as FieldActivityUpdate,
      );
    } else {
      await activityStore.createActivity(data as FieldActivityCreate);
    }
    closeActivityForm();
    await loadActivities(activityStore.filters);
  } catch (error: any) {
    console.error("Failed to save activity:", error);
    alert(
      error.response?.data?.detail ||
        "Failed to save activity. Please try again.",
    );
  } finally {
    formLoading.value = false;
  }
};

const closeActivityForm = () => {
  showActivityForm.value = false;
  editingActivity.value = null;
};

onMounted(async () => {
  // Load workspace to get members for staff filter
  if (currentWorkspaceId.value && !currentWorkspace.value) {
    await workspaceStore.fetchWorkspace(currentWorkspaceId.value);
  }
  loadActivities();
});
</script>
