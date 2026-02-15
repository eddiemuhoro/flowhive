<!-- Activity Card Component -->
<!-- Displays a field activity in a compact card format for lists -->

<template>
  <div
    class="rounded-lg border bg-white p-4 shadow-sm transition-all hover:shadow-md"
    :class="{ 'border-l-4': activity.task_category }"
    :style="categoryBorderStyle"
  >
    <!-- Header -->
    <div class="mb-3 flex items-start justify-between">
      <div class="flex-1">
        <h3 class="text-base font-semibold text-gray-900">
          {{ activity.title }}
        </h3>
        <p class="mt-1 text-sm text-gray-600">{{ activity.customer_name }}</p>
      </div>
      <CategoryBadge
        v-if="activity.task_category"
        :category="activity.task_category"
        :show-title="true"
      />
    </div>

    <!-- Details Grid -->
    <div class="grid grid-cols-2 gap-3 text-sm">
      <!-- Location -->
      <div class="flex items-center space-x-2 text-gray-600">
        <svg
          class="h-4 w-4 flex-shrink-0"
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
        <span class="truncate">{{ activity.location }}</span>
      </div>

      <!-- Duration -->
      <div class="flex items-center space-x-2 text-gray-600">
        <svg
          class="h-4 w-4 flex-shrink-0"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <span>{{ activity.duration_hours ? formatDuration(activity.duration_hours) : 'N/A' }}</span>
      </div>

      <!-- Support Staff -->
      <div class="flex items-center space-x-2 text-gray-600">
        <svg
          class="h-4 w-4 flex-shrink-0"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
          />
        </svg>
        <span class="truncate">{{ activity.support_staff_name }}</span>
      </div>

      <!-- Date & Time -->
      <div class="flex items-center space-x-2 text-gray-600">
        <svg
          class="h-4 w-4 flex-shrink-0"
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
        <span>{{ formatDateTime }}</span>
      </div>
    </div>

    <!-- Task Description -->
    <div
      v-if="showDescription && activity.task_description"
      class="mt-3 border-t pt-3"
    >
      <div class="prose prose-sm text-sm text-gray-700 line-clamp-2" v-html="activity.task_description"></div>
    </div>

    <!-- Customer Rep -->
    <div
      v-if="activity.customer_rep"
      class="mt-3 flex items-center justify-between border-t pt-3 text-xs text-gray-500"
    >
      <span
        >Customer Rep:
        <span class="font-medium text-gray-700">{{
          activity.customer_rep
        }}</span></span
      >
    </div>

    <!-- Actions -->
    <div
      v-if="showActions"
      class="mt-4 flex items-center justify-end space-x-2 border-t pt-3"
    >
      <button
        @click.stop="$emit('view', activity.id)"
        class="rounded-lg px-3 py-1.5 text-sm font-medium text-blue-600 hover:bg-blue-50"
      >
        View Details
      </button>
      <button
        v-if="canEdit"
        @click.stop="$emit('edit', activity.id)"
        class="rounded-lg px-3 py-1.5 text-sm font-medium text-gray-600 hover:bg-gray-100"
      >
        Edit
      </button>
      <button
        v-if="canDelete"
        @click.stop="$emit('delete', activity.id)"
        class="rounded-lg px-3 py-1.5 text-sm font-medium text-red-600 hover:bg-red-50"
      >
        Delete
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import CategoryBadge from "@/components/field/category/CategoryBadge.vue";
import type { FieldActivity } from "@/types/field";

interface Props {
  activity: FieldActivity;
  showDescription?: boolean;
  showActions?: boolean;
}

interface Emits {
  (e: "view", id: number): void;
  (e: "edit", id: number): void;
  (e: "delete", id: number): void;
}

const props = withDefaults(defineProps<Props>(), {
  showDescription: true,
  showActions: true,
});

defineEmits<Emits>();

const authStore = useAuthStore();
const currentUser = computed(() => authStore.user);

const canEdit = computed(() => {
  const role = currentUser.value?.role?.toUpperCase();
  return (
    currentUser.value?.id === props.activity.created_by ||
    role === "MANAGER" ||
    role === "EXECUTIVE"
  );
});

const canDelete = computed(() => {
  const role = currentUser.value?.role?.toUpperCase();
  return (
    currentUser.value?.id === props.activity.created_by ||
    role === "MANAGER" ||
    role === "EXECUTIVE"
  );
});

const categoryBorderStyle = computed(() => {
  if (!props.activity.task_category?.color) return {};
  return {
    borderLeftColor: props.activity.task_category.color,
  };
});

const formatDateTime = computed(() => {
  const date = new Date(props.activity.activity_date);
  const formattedDate = date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  });
  const time = props.activity.start_time?.substring(0, 5) || 'TBD'; // HH:MM
  return `${formattedDate} • ${time}`;
});

const formatDuration = (hours: number): string => {
  if (hours < 1) {
    const minutes = Math.round(hours * 60);
    return `${minutes}m`;
  }
  const fullHours = Math.floor(hours);
  const minutes = Math.round((hours - fullHours) * 60);
  return minutes > 0 ? `${fullHours}h ${minutes}m` : `${fullHours}h`;
};
</script>
