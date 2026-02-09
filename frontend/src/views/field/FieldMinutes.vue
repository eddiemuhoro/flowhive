<!-- Field Minutes View -->
<!-- Meeting minutes listing and management for field operations -->

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <div class="mx-auto max-w-7xl space-y-6">
      <!-- Header -->
      <div
        class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
      >
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Meeting Minutes</h1>
          <p class="mt-1 text-sm text-gray-600">
            Document and track field meetings
          </p>
        </div>
        <button
          @click="showCreateModal = true"
          class="flex items-center justify-center space-x-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-blue-700 active:scale-95"
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
          <span>New Minutes</span>
        </button>
      </div>

      <!-- Filters -->
      <div class="rounded-lg bg-white p-4 shadow-sm">
        <div class="grid gap-4 sm:grid-cols-3">
          <div>
            <label class="block text-sm font-medium text-gray-700"
              >From Date</label
            >
            <input
              v-model="filters.date_from"
              type="date"
              class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700"
              >To Date</label
            >
            <input
              v-model="filters.date_to"
              type="date"
              class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700"
              >Search</label
            >
            <input
              v-model="filters.search"
              type="text"
              placeholder="Search minutes..."
              class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            />
          </div>
        </div>
        <div class="mt-4 flex justify-end">
          <button
            @click="applyFilters"
            class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            Apply Filters
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center py-12">
        <div
          class="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"
        ></div>
      </div>

      <!-- Minutes List -->
      <div v-else-if="minutes.length > 0" class="space-y-4">
        <div
          v-for="minute in minutes"
          :key="minute.id"
          @click="viewMinute(minute.id)"
          class="cursor-pointer rounded-lg bg-white p-4 shadow-sm transition-shadow hover:shadow-md"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-gray-900">
                {{ minute.title }}
              </h3>
              <div
                class="mt-2 flex flex-wrap items-center gap-3 text-sm text-gray-600"
              >
                <span class="flex items-center">
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
                      d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                    />
                  </svg>
                  {{ formatDate(minute.meeting_date) }}
                </span>
                <span v-if="minute.location" class="flex items-center">
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
                      d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                    />
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                  </svg>
                  {{ minute.location }}
                </span>
                <span
                  v-if="minute.attendees && minute.attendees.length"
                  class="flex items-center"
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
                      d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                    />
                  </svg>
                  {{ minute.attendees.length }} attendees
                </span>
              </div>
            </div>
            <div class="flex gap-2">
              <span
                v-if="minute.attachment_count > 0"
                class="flex items-center text-sm text-gray-500"
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
                    d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"
                  />
                </svg>
                {{ minute.attachment_count }}
              </span>
              <span
                v-if="minute.action_item_count > 0"
                class="flex items-center text-sm text-gray-500"
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
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                  />
                </svg>
                {{ minute.action_item_count }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="rounded-lg bg-white p-12 text-center shadow-sm">
        <svg
          class="mx-auto h-16 w-16 text-gray-400"
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
        <h3 class="mt-4 text-lg font-medium text-gray-900">
          No meeting minutes yet
        </h3>
        <p class="mt-2 text-sm text-gray-600">
          Get started by creating your first meeting minutes.
        </p>
        <button
          @click="showCreateModal = true"
          class="mt-4 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          Create Minutes
        </button>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <Teleport to="body">
      <div
        v-if="showCreateModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
        @click.self="closeModal"
      >
        <div
          class="max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-lg bg-white p-6 shadow-xl"
        >
          <div class="mb-4 flex items-center justify-between">
            <div>
              <h2 class="text-xl font-bold text-gray-900">
                New Meeting Minutes
              </h2>
              <p class="mt-1 text-sm text-gray-600">
                Fill in details or upload a PDF with title and date
              </p>
            </div>
            <button
              @click="closeModal"
              class="rounded-lg p-1 hover:bg-gray-100"
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

          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700"
                >Title *</label
              >
              <input
                v-model="form.title"
                required
                type="text"
                class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2"
                placeholder="e.g., Weekly Team Meeting"
              />
            </div>

            <div class="grid gap-4 sm:grid-cols-3">
              <div>
                <label class="block text-sm font-medium text-gray-700"
                  >Date *</label
                >
                <input
                  v-model="form.meeting_date"
                  required
                  type="date"
                  class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700"
                  >Start Time</label
                >
                <input
                  v-model="form.meeting_time_start"
                  type="time"
                  class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700"
                  >End Time</label
                >
                <input
                  v-model="form.meeting_time_end"
                  type="time"
                  class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700"
                >Location</label
              >
              <input
                v-model="form.location"
                type="text"
                class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2"
                placeholder="Meeting location"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700"
                >Agenda</label
              >
              <textarea
                v-model="form.agenda"
                rows="3"
                class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2"
                placeholder="Meeting agenda..."
              ></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700"
                >Discussions</label
              >
              <textarea
                v-model="form.discussions"
                rows="4"
                class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2"
                placeholder="Key discussions and points raised..."
              ></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700"
                >Decisions</label
              >
              <textarea
                v-model="form.decisions"
                rows="3"
                class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2"
                placeholder="Decisions made during the meeting..."
              ></textarea>
            </div>

            <!-- PDF Upload Section -->
            <div class="rounded-lg border-2 border-dashed border-gray-300 p-4">
              <div class="flex items-center justify-between mb-2">
                <label class="block text-sm font-medium text-gray-700">
                  Attach Files (Optional)
                </label>
                <span class="text-xs text-gray-500">PDF, Images, Docs</span>
              </div>
              <input
                ref="fileInput"
                type="file"
                multiple
                accept=".pdf,.doc,.docx,.xls,.xlsx,image/*"
                @change="handleFileSelect"
                class="hidden"
              />
              <button
                type="button"
                @click="fileInput?.click()"
                class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                <svg
                  class="mx-auto mb-2 h-8 w-8 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  />
                </svg>
                Click to select files
              </button>

              <!-- Selected Files List -->
              <div v-if="selectedFiles.length > 0" class="mt-3 space-y-2">
                <div
                  v-for="(file, index) in selectedFiles"
                  :key="index"
                  class="flex items-center justify-between rounded-lg border border-gray-200 bg-gray-50 px-3 py-2"
                >
                  <div class="flex items-center space-x-2">
                    <svg
                      v-if="file.type === 'application/pdf'"
                      class="h-5 w-5 text-red-500"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                      />
                    </svg>
                    <svg
                      v-else
                      class="h-5 w-5 text-blue-500"
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
                      <p class="text-sm font-medium text-gray-900">
                        {{ file.name }}
                      </p>
                      <p class="text-xs text-gray-500">
                        {{ formatFileSize(file.size) }}
                      </p>
                    </div>
                  </div>
                  <button
                    type="button"
                    @click="removeFile(index)"
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
            </div>

            <div class="flex justify-end gap-3 pt-4">
              <button
                type="button"
                @click="closeModal"
                class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
              >
                {{ submitting ? "Creating..." : "Create Minutes" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useMeetingMinuteStore } from "@/stores/meetingMinute";
import { useWorkspaceStore } from "@/stores/workspace";
import type { MeetingMinuteFilters } from "@/types/meetingMinute";

const router = useRouter();
const minuteStore = useMeetingMinuteStore();
const workspaceStore = useWorkspaceStore();

const showCreateModal = ref(false);
const submitting = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);
const selectedFiles = ref<File[]>([]);

const filters = ref<MeetingMinuteFilters>({
  date_from: "",
  date_to: "",
  search: "",
});

const form = ref({
  title: "",
  meeting_date: new Date().toISOString().split("T")[0],
  meeting_time_start: "",
  meeting_time_end: "",
  location: "",
  agenda: "",
  discussions: "",
  decisions: "",
});

const minutes = computed(() => minuteStore.minutes);
const loading = computed(() => minuteStore.loading);
const currentWorkspaceId = computed(
  () => workspaceStore.currentWorkspace?.id || 0,
);

onMounted(async () => {
  if (currentWorkspaceId.value) {
    await minuteStore.fetchMinutes(currentWorkspaceId.value);
  }
});

const applyFilters = async () => {
  if (currentWorkspaceId.value) {
    await minuteStore.fetchMinutes(
      currentWorkspaceId.value,
      filters.value.date_from || filters.value.date_to || filters.value.search
        ? filters.value
        : undefined,
    );
  }
};

const handleSubmit = async () => {
  if (!currentWorkspaceId.value) return;

  submitting.value = true;
  try {
    // Create the meeting minute
    const newMinute = await minuteStore.createMinute({
      workspace_id: currentWorkspaceId.value,
      ...form.value,
      meeting_time_start: form.value.meeting_time_start || null,
      meeting_time_end: form.value.meeting_time_end || null,
      location: form.value.location || null,
      agenda: form.value.agenda || null,
      discussions: form.value.discussions || null,
      decisions: form.value.decisions || null,
    });

    // Upload any attached files
    if (selectedFiles.value.length > 0) {
      for (const file of selectedFiles.value) {
        try {
          await minuteStore.uploadAttachment(newMinute.id, file);
        } catch (uploadError: any) {
          console.error("Failed to upload file:", uploadError);
          // Continue with other files even if one fails
        }
      }
    }

    closeModal();
    router.push(`/field/minutes/${newMinute.id}`);
  } catch (error: any) {
    console.error("Failed to create minute:", error);
    alert(error.response?.data?.detail || "Failed to create meeting minutes");
  } finally {
    submitting.value = false;
  }
};

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    selectedFiles.value.push(...Array.from(target.files));
    target.value = ""; // Reset input
  }
};

const removeFile = (index: number) => {
  selectedFiles.value.splice(index, 1);
};

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

const closeModal = () => {
  showCreateModal.value = false;
  selectedFiles.value = [];
  form.value = {
    title: "",
    meeting_date: new Date().toISOString().split("T")[0],
    meeting_time_start: "",
    meeting_time_end: "",
    location: "",
    agenda: "",
    discussions: "",
    decisions: "",
  };
};

const viewMinute = (id: number) => {
  router.push(`/field/minutes/${id}`);
};

const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};
</script>
