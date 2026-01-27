<!-- Field Activity Detail View -->
<!-- Detailed view of a single field activity with photos -->

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <div class="mx-auto max-w-4xl space-y-6">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-12">
        <div class="text-center">
          <div
            class="inline-block h-12 w-12 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"
          ></div>
          <p class="mt-2 text-sm text-gray-600">Loading activity...</p>
        </div>
      </div>

      <!-- Activity Not Found -->
      <div
        v-else-if="!activity"
        class="rounded-lg bg-white p-12 text-center shadow-sm"
      >
        <svg
          class="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <h3 class="mt-2 text-lg font-medium text-gray-900">
          Activity Not Found
        </h3>
        <p class="mt-1 text-sm text-gray-500">
          The activity you're looking for doesn't exist or has been deleted.
        </p>
        <button
          @click="goBack"
          class="mt-4 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          Go Back
        </button>
      </div>

      <!-- Activity Content -->
      <template v-else>
        <!-- Header with Actions -->
        <div class="flex items-start justify-between">
          <button
            @click="goBack"
            class="flex items-center space-x-2 text-sm font-medium text-gray-600 hover:text-gray-900"
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
                d="M15 19l-7-7 7-7"
              />
            </svg>
            <span>Back to Activities</span>
          </button>

          <div class="flex items-center space-x-2">
            <button
              v-if="canEdit"
              @click="showEditForm = true"
              class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Edit
            </button>
            <button
              v-if="canDelete"
              @click="handleDelete"
              class="rounded-lg border border-red-300 px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50"
            >
              Delete
            </button>
          </div>
        </div>

        <!-- Main Activity Card -->
        <div class="rounded-lg bg-white p-6 shadow-sm">
          <!-- Title and Category -->
          <div class="mb-4 flex items-start justify-between">
            <div class="flex-1">
              <h1 class="text-2xl font-bold text-gray-900">
                {{ activity.title }}
              </h1>
              <p class="mt-1 text-lg text-gray-700">
                {{ activity.customer_name }}
              </p>
            </div>
            <CategoryBadge
              v-if="activity.task_category"
              :category="activity.task_category"
            />
          </div>

          <!-- Details Grid -->
          <div class="grid grid-cols-1 gap-6 border-t pt-6 md:grid-cols-2">
            <!-- Date & Time -->
            <div>
              <h3 class="text-sm font-medium text-gray-500">Date & Time</h3>
              <p class="mt-1 text-base text-gray-900">
                {{ formatDate(activity.activity_date) }}
              </p>
              <p class="mt-1 text-sm text-gray-600">
                {{ activity.start_time.substring(0, 5) }} -
                {{ activity.end_time.substring(0, 5) }}
                <span class="ml-2 text-gray-500"
                  >({{ formatDuration(activity.duration_hours) }})</span
                >
              </p>
            </div>

            <!-- Support Staff -->
            <div>
              <h3 class="text-sm font-medium text-gray-500">Support Staff</h3>
              <p class="mt-1 text-base text-gray-900">
                {{ activity.support_staff_name }}
              </p>
            </div>

            <!-- Location -->
            <div>
              <h3 class="text-sm font-medium text-gray-500">Location</h3>
              <p class="mt-1 text-base text-gray-900">
                {{ activity.location }}
              </p>
            </div>

            <!-- Customer Representative -->
            <div>
              <h3 class="text-sm font-medium text-gray-500">
                Customer Representative
              </h3>
              <p class="mt-1 text-base text-gray-900">
                {{ activity.customer_rep }}
              </p>
            </div>
          </div>

          <!-- Task Description -->
          <div class="mt-6 border-t pt-6">
            <h3 class="text-sm font-medium text-gray-500">Task Description</h3>
            <p class="mt-2 whitespace-pre-wrap text-base text-gray-900">
              {{ activity.task_description }}
            </p>
          </div>

          <!-- Remarks -->
          <div v-if="activity.remarks" class="mt-6 border-t pt-6">
            <h3 class="text-sm font-medium text-gray-500">Remarks</h3>
            <p class="mt-2 whitespace-pre-wrap text-base text-gray-900">
              {{ activity.remarks }}
            </p>
          </div>

          <!-- Metadata -->
          <div class="mt-6 border-t pt-6">
            <div
              class="grid grid-cols-1 gap-4 text-xs text-gray-500 md:grid-cols-2"
            >
              <div>
                <span class="font-medium">Created by:</span>
                {{ activity.created_by_name }}
                <span class="ml-1"
                  >on {{ formatDateTime(activity.created_at) }}</span
                >
              </div>
              <div v-if="activity.updated_by">
                <span class="font-medium">Last updated by:</span>
                {{ activity.updated_by_name }}
                <span class="ml-1"
                  >on {{ formatDateTime(activity.updated_at) }}</span
                >
              </div>
            </div>
          </div>
        </div>

        <!-- Photos Section -->
        <div class="rounded-lg bg-white p-6 shadow-sm">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-900">
              Photos
              <span
                v-if="activity.photos.length > 0"
                class="ml-2 text-sm font-normal text-gray-500"
              >
                ({{ activity.photos.length }})
              </span>
            </h2>
            <button
              v-if="canEdit"
              @click="showPhotoUpload = true"
              class="text-sm font-medium text-blue-600 hover:text-blue-700"
            >
              + Add Photos
            </button>
          </div>

          <!-- Photo Gallery -->
          <PhotoGallery
            :photos="activity.photos"
            :can-delete="canEdit"
            @delete="handlePhotoDelete"
          />
        </div>

        <!-- Photo Upload Section -->
        <div v-if="showPhotoUpload" class="rounded-lg bg-white p-6 shadow-sm">
          <h3 class="mb-4 text-lg font-semibold text-gray-900">
            Upload Photos
          </h3>
          <PhotoUpload
            ref="photoUploadRef"
            :disabled="uploadingPhotos"
            @upload="handlePhotoUpload"
          />
        </div>
      </template>
    </div>

    <!-- Edit Activity Modal -->
    <Teleport to="body">
      <div
        v-if="showEditForm"
        class="fixed inset-0 z-50 overflow-y-auto bg-black/50 p-4"
        @click.self="closeEditForm"
      >
        <div class="mx-auto max-w-2xl rounded-lg bg-white p-6 shadow-xl">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-semibold text-gray-900">Edit Activity</h2>
            <button
              @click="closeEditForm"
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
            v-if="activity"
            :workspace-id="currentWorkspaceId"
            :activity="activity"
            :loading="formLoading"
            @submit="handleActivityUpdate"
            @cancel="closeEditForm"
          />
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useWorkspaceStore } from "@/stores/workspace";
import { useFieldActivityStore } from "@/stores/fieldActivity";
import CategoryBadge from "@/components/field/category/CategoryBadge.vue";
import PhotoGallery from "@/components/field/photo/PhotoGallery.vue";
import PhotoUpload from "@/components/field/photo/PhotoUpload.vue";
import ActivityForm from "@/components/field/activity/ActivityForm.vue";
import type { FieldActivityUpdate, FieldActivityCreate } from "@/types/field";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const workspaceStore = useWorkspaceStore();
const activityStore = useFieldActivityStore();

const activityId = computed(() => Number(route.params.id));
const currentUser = computed(() => authStore.user);
const currentWorkspace = computed(() => workspaceStore.currentWorkspace);
const currentWorkspaceId = computed(() => currentWorkspace.value?.id || 0);
const activity = computed(() => activityStore.currentActivity);

const loading = ref(false);
const formLoading = ref(false);
const showEditForm = ref(false);
const showPhotoUpload = ref(false);
const uploadingPhotos = ref(false);
const photoUploadRef = ref<any>(null);

const canEdit = computed(() => {
  if (!activity.value || !currentUser.value) return false;
  const role = currentUser.value.role?.toUpperCase();
  return (
    currentUser.value.id === activity.value.created_by ||
    role === "MANAGER" ||
    role === "EXECUTIVE"
  );
});

const canDelete = computed(() => canEdit.value);

const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr);
  return date.toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const formatDateTime = (dateStr: string): string => {
  const date = new Date(dateStr);
  return date.toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
};

const formatDuration = (hours: number): string => {
  if (hours < 1) {
    const minutes = Math.round(hours * 60);
    return `${minutes} minutes`;
  }
  const fullHours = Math.floor(hours);
  const minutes = Math.round((hours - fullHours) * 60);
  return minutes > 0 ? `${fullHours}h ${minutes}m` : `${fullHours} hours`;
};

const loadActivity = async () => {
  loading.value = true;
  try {
    await activityStore.fetchActivity(
      activityId.value,
      currentWorkspaceId.value,
    );
  } catch (error) {
    console.error("Failed to load activity:", error);
  } finally {
    loading.value = false;
  }
};

const handleActivityUpdate = async (
  data: FieldActivityCreate | FieldActivityUpdate,
) => {
  formLoading.value = true;
  try {
    await activityStore.updateActivity(
      activityId.value,
      currentWorkspaceId.value,
      data as FieldActivityUpdate,
    );
    closeEditForm();
    await loadActivity();
  } catch (error: any) {
    console.error("Failed to update activity:", error);
    alert(
      error.response?.data?.detail ||
        "Failed to update activity. Please try again.",
    );
  } finally {
    formLoading.value = false;
  }
};

const handleDelete = async () => {
  if (
    !confirm(
      "Are you sure you want to delete this activity? This action cannot be undone.",
    )
  ) {
    return;
  }

  try {
    await activityStore.deleteActivity(
      activityId.value,
      currentWorkspaceId.value,
    );
    router.push("/field/activities");
  } catch (error: any) {
    console.error("Failed to delete activity:", error);
    alert(
      error.response?.data?.detail ||
        "Failed to delete activity. Please try again.",
    );
  }
};

const handlePhotoUpload = async (files: File[]) => {
  uploadingPhotos.value = true;

  try {
    for (const file of files) {
      await activityStore.uploadPhoto(
        activityId.value,
        currentWorkspaceId.value,
        file,
      );
      photoUploadRef.value?.markAsUploaded(file.name);
    }
    showPhotoUpload.value = false;
    await loadActivity();
  } catch (error: any) {
    console.error("Failed to upload photos:", error);
    alert(
      error.response?.data?.detail ||
        "Failed to upload photos. Please try again.",
    );
  } finally {
    uploadingPhotos.value = false;
  }
};

const handlePhotoDelete = async (photoId: number) => {
  try {
    await activityStore.deletePhoto(
      activityId.value,
      photoId,
      currentWorkspaceId.value,
    );
  } catch (error: any) {
    console.error("Failed to delete photo:", error);
    alert(
      error.response?.data?.detail ||
        "Failed to delete photo. Please try again.",
    );
  }
};

const closeEditForm = () => {
  showEditForm.value = false;
};

const goBack = () => {
  router.push("/field/activities");
};

onMounted(() => {
  loadActivity();
});
</script>
