<!-- Field Minute Detail View -->
<!-- View and edit a single meeting minute with attachments and action items -->

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <div class="mx-auto max-w-4xl space-y-6">
      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-12">
        <div
          class="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"
        ></div>
      </div>

      <template v-else-if="minute">
        <!-- Header -->
        <div class="flex items-start justify-between">
          <button
            @click="router.back()"
            class="flex items-center text-sm text-gray-600 hover:text-gray-900"
          >
            <svg
              class="mr-1 h-4 w-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
            Back
          </button>
          <button
            @click="confirmDelete"
            class="text-sm text-red-600 hover:text-red-700"
          >
            Delete
          </button>
        </div>

        <!-- Minute Details Card -->
        <div class="rounded-lg bg-white p-6 shadow-sm">
          <h1 class="text-2xl font-bold text-gray-900">{{ minute.title }}</h1>

          <div class="mt-4 grid gap-4 sm:grid-cols-2">
            <div>
              <span class="text-sm font-medium text-gray-500">Date</span>
              <p class="mt-1 text-gray-900">
                {{ formatDate(minute.meeting_date) }}
              </p>
            </div>
            <div v-if="minute.meeting_time_start">
              <span class="text-sm font-medium text-gray-500">Time</span>
              <p class="mt-1 text-gray-900">
                {{ minute.meeting_time_start }}
                <span v-if="minute.meeting_time_end"
                  >- {{ minute.meeting_time_end }}</span
                >
              </p>
            </div>
            <div v-if="minute.location">
              <span class="text-sm font-medium text-gray-500">Location</span>
              <p class="mt-1 text-gray-900">{{ minute.location }}</p>
            </div>
            <div v-if="minute.attendees && minute.attendees.length">
              <span class="text-sm font-medium text-gray-500">Attendees</span>
              <p class="mt-1 text-gray-900">
                {{ minute.attendees.map((a) => a.name).join(", ") }}
              </p>
            </div>
          </div>

          <div v-if="minute.agenda" class="mt-6">
            <h3 class="text-sm font-semibold text-gray-700">Agenda</h3>
            <div class="mt-2 text-gray-900 whitespace-pre-wrap">
              {{ minute.agenda }}
            </div>
          </div>

          <div v-if="minute.discussions" class="mt-6">
            <h3 class="text-sm font-semibold text-gray-700">Discussions</h3>
            <div class="mt-2 text-gray-900 whitespace-pre-wrap">
              {{ minute.discussions }}
            </div>
          </div>

          <div v-if="minute.decisions" class="mt-6">
            <h3 class="text-sm font-semibold text-gray-700">Decisions</h3>
            <div class="mt-2 text-gray-900 whitespace-pre-wrap">
              {{ minute.decisions }}
            </div>
          </div>
        </div>

        <!-- Attachments -->
        <div class="rounded-lg bg-white p-6 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold text-gray-900">
              Attachments
              <span
                v-if="minute.attachments.length"
                class="ml-2 text-sm font-normal text-gray-500"
              >
                ({{ minute.attachments.length }})
              </span>
            </h2>
            <button
              @click="triggerFileUpload"
              class="text-sm font-medium text-blue-600 hover:text-blue-700"
            >
              + Add Files
            </button>
          </div>

          <input
            ref="fileInput"
            type="file"
            multiple
            accept=".pdf,.doc,.docx,.xls,.xlsx,image/*"
            @change="handleFileUpload"
            class="hidden"
          />

          <div v-if="minute.attachments.length" class="space-y-2">
            <div
              v-for="attachment in minute.attachments"
              :key="attachment.id"
              class="flex items-center justify-between rounded-lg border border-gray-200 p-3"
            >
              <div class="flex items-center space-x-3">
                <svg
                  v-if="attachment.mime_type.startsWith('image')"
                  class="h-8 w-8 text-blue-500"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
                <svg
                  v-else
                  class="h-8 w-8 text-gray-500"
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
                <div>
                  <a
                    :href="attachment.cloudinary_url"
                    target="_blank"
                    class="text-sm font-medium text-blue-600 hover:underline"
                  >
                    {{ attachment.file_name }}
                  </a>
                  <p class="text-xs text-gray-500">
                    {{ formatFileSize(attachment.file_size) }}
                  </p>
                </div>
              </div>
              <button
                @click="deleteAttachment(attachment.id)"
                class="text-red-600 hover:text-red-700"
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
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                  />
                </svg>
              </button>
            </div>
          </div>

          <p v-else class="text-sm text-gray-500">No attachments yet</p>
        </div>

        <!-- Action Items -->
        <div class="rounded-lg bg-white p-6 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold text-gray-900">
              Action Items
              <span
                v-if="minute.action_items.length"
                class="ml-2 text-sm font-normal text-gray-500"
              >
                ({{ minute.action_items.length }})
              </span>
            </h2>
            <button
              @click="showActionItemForm = !showActionItemForm"
              class="text-sm font-medium text-blue-600 hover:text-blue-700"
            >
              + Add Action Item
            </button>
          </div>

          <!-- Action Item Form -->
          <form
            v-if="showActionItemForm"
            @submit.prevent="createActionItem"
            class="mb-4 space-y-3 rounded-lg border border-gray-200 p-4"
          >
            <input
              v-model="actionItemForm.description"
              required
              type="text"
              placeholder="Action item description..."
              class="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            />
            <div class="flex gap-3">
              <input
                v-model="actionItemForm.due_date"
                type="date"
                class="block flex-1 rounded-lg border border-gray-300 px-3 py-2 text-sm"
              />
              <select
                v-model="actionItemForm.status"
                class="block rounded-lg border border-gray-300 px-3 py-2 text-sm"
              >
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>
            <div class="flex justify-end gap-2">
              <button
                type="button"
                @click="showActionItemForm = false"
                class="rounded-lg border border-gray-300 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="rounded-lg bg-blue-600 px-3 py-1.5 text-sm text-white hover:bg-blue-700"
              >
                Add
              </button>
            </div>
          </form>

          <!-- Action Items List -->
          <div v-if="minute.action_items.length" class="space-y-2">
            <div
              v-for="item in minute.action_items"
              :key="item.id"
              class="flex items-center justify-between rounded-lg border border-gray-200 p-3"
            >
              <div class="flex-1">
                <p class="text-sm font-medium text-gray-900">
                  {{ item.description }}
                </p>
                <div class="mt-1 flex items-center gap-3 text-xs text-gray-500">
                  <span v-if="item.due_date"
                    >Due: {{ formatDate(item.due_date) }}</span
                  >
                  <span
                    :class="{
                      'text-yellow-600': item.status === 'pending',
                      'text-blue-600': item.status === 'in_progress',
                      'text-green-600': item.status === 'completed',
                    }"
                  >
                    {{ item.status }}
                  </span>
                </div>
              </div>
              <button
                @click="deleteActionItem(item.id)"
                class="text-red-600 hover:text-red-700"
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
          </div>

          <p v-else class="text-sm text-gray-500">No action items yet</p>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useMeetingMinuteStore } from "@/stores/meetingMinute";
import { useWorkspaceStore } from "@/stores/workspace";

const router = useRouter();
const route = useRoute();
const minuteStore = useMeetingMinuteStore();
const workspaceStore = useWorkspaceStore();

const fileInput = ref<HTMLInputElement | null>(null);
const showActionItemForm = ref(false);
const actionItemForm = ref({
  description: "",
  due_date: "",
  status: "pending",
});

const minuteId = computed(() => Number(route.params.id));
const minute = computed(() => minuteStore.currentMinute);
const loading = computed(() => minuteStore.loading);
const currentWorkspaceId = computed(
  () => workspaceStore.currentWorkspace?.id || 0,
);

onMounted(async () => {
  if (minuteId.value) {
    await minuteStore.fetchMinute(minuteId.value);
  }
});

const triggerFileUpload = () => {
  fileInput.value?.click();
};

const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (!target.files || target.files.length === 0) return;

  for (const file of Array.from(target.files)) {
    try {
      await minuteStore.uploadAttachment(minuteId.value, file);
    } catch (error: any) {
      console.error("Failed to upload file:", error);
      alert(error.response?.data?.detail || "Failed to upload file");
    }
  }

  target.value = "";
};

const deleteAttachment = async (attachmentId: number) => {
  if (!confirm("Are you sure you want to delete this attachment?")) return;

  try {
    await minuteStore.deleteAttachment(minuteId.value, attachmentId);
  } catch (error: any) {
    console.error("Failed to delete attachment:", error);
    alert(error.response?.data?.detail || "Failed to delete attachment");
  }
};

const createActionItem = async () => {
  try {
    await minuteStore.createActionItem(minuteId.value, {
      description: actionItemForm.value.description,
      due_date: actionItemForm.value.due_date || null,
      status: actionItemForm.value.status,
    });

    showActionItemForm.value = false;
    actionItemForm.value = {
      description: "",
      due_date: "",
      status: "pending",
    };
  } catch (error: any) {
    console.error("Failed to create action item:", error);
    alert(error.response?.data?.detail || "Failed to create action item");
  }
};

const deleteActionItem = async (actionItemId: number) => {
  if (!confirm("Are you sure you want to delete this action item?")) return;

  try {
    await minuteStore.deleteActionItem(minuteId.value, actionItemId);
  } catch (error: any) {
    console.error("Failed to delete action item:", error);
    alert(error.response?.data?.detail || "Failed to delete action item");
  }
};

const confirmDelete = async () => {
  if (
    !confirm(
      "Are you sure you want to delete this meeting minute? This cannot be undone.",
    )
  )
    return;

  try {
    await minuteStore.deleteMinute(minuteId.value);
    router.push("/field/minutes");
  } catch (error: any) {
    console.error("Failed to delete minute:", error);
    alert(error.response?.data?.detail || "Failed to delete minute");
  }
};

const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};
</script>
