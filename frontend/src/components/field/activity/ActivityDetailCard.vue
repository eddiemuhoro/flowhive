<!-- Activity Detail Card Component -->
<!-- Displays complete activity information for reports -->

<template>
  <div class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
    <!-- Header with Number -->
    <div class="mb-4 flex items-start justify-between">
      <div class="flex items-start space-x-3">
        <div
          class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-blue-100 text-sm font-semibold text-blue-700"
        >
          {{ index }}
        </div>
        <div>
          <h3 class="text-base font-semibold text-gray-900">
            {{ activity.title }}
          </h3>
          <div class="mt-1 flex items-center space-x-3 text-sm text-gray-600">
            <span>{{ formatDate(activity.activity_date) }}</span>
            <span>·</span>
            <span
              >{{ formatTime(activity.start_time || '') }} -
              {{ formatTime(activity.end_time || '') }}</span
            >
            <span>·</span>
            <span class="font-medium"
              >{{ activity.duration_hours?.toFixed(1) || "0.0" }} hours</span
            >
          </div>
        </div>
      </div>
      <CategoryBadge
        v-if="activity.task_category"
        :category="activity.task_category"
        :show-title="true"
      />
    </div>

    <!-- Information Grid -->
    <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
      <!-- Support Staff -->
      <div>
        <dt class="text-xs font-medium text-gray-500">Support Staff</dt>
        <dd class="mt-1 text-sm text-gray-900">
          {{ activity.support_staff_name }}
        </dd>
      </div>

      <!-- Customer -->
      <div>
        <dt class="text-xs font-medium text-gray-500">Customer</dt>
        <dd class="mt-1 text-sm text-gray-900">
          {{ activity.customer_name }}
        </dd>
      </div>

      <!-- Location -->
      <div>
        <dt class="text-xs font-medium text-gray-500">Location</dt>
        <dd class="mt-1 text-sm text-gray-900">{{ activity.location }}</dd>
      </div>

      <!-- Customer Representative -->
      <div v-if="activity.customer_rep">
        <dt class="text-xs font-medium text-gray-500">Customer Rep</dt>
        <dd class="mt-1 text-sm text-gray-900">{{ activity.customer_rep }}</dd>
      </div>
    </div>

    <!-- Task Description -->
    <div v-if="activity.task_description" class="mt-4 border-t pt-4">
      <dt class="text-xs font-medium text-gray-500">Task Description</dt>
      <dd
        class="prose prose-sm mt-2 max-w-none text-sm text-gray-900"
        v-html="activity.task_description"
      ></dd>
    </div>

    <!-- Remarks -->
    <div v-if="activity.remarks" class="mt-4 border-t pt-4">
      <dt class="text-xs font-medium text-gray-500">Remarks</dt>
      <dd class="mt-2 text-sm text-gray-900">{{ activity.remarks }}</dd>
    </div>

    <!-- Footer Metadata -->
    <div class="mt-4 border-t pt-3 text-xs text-gray-500">
      <span
        >Created by {{ activity.created_by_name }} on
        {{ formatDateTime(activity.created_at) }}</span
      >
      <span v-if="activity.updated_by_name" class="ml-3"
        >· Updated by {{ activity.updated_by_name }} on
        {{ formatDateTime(activity.updated_at) }}</span
      >
    </div>
  </div>
</template>

<script setup lang="ts">
import CategoryBadge from "@/components/field/category/CategoryBadge.vue";
import type { FieldActivity } from "@/types/field";

interface Props {
  activity: FieldActivity;
  index?: number;
}

withDefaults(defineProps<Props>(), {
  index: 1,
});

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const formatTime = (timeStr: string) => {
  // timeStr is in HH:MM:SS format
  const [hours, minutes] = timeStr.split(":");
  const hour = parseInt(hours, 10);
  const ampm = hour >= 12 ? "PM" : "AM";
  const displayHour = hour % 12 || 12;
  return `${displayHour}:${minutes} ${ampm}`;
};

const formatDateTime = (dateTimeStr: string) => {
  const date = new Date(dateTimeStr);
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};
</script>
