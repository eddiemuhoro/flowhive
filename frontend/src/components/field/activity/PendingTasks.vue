<!-- Pending Tasks Component -->
<!-- Display tasks assigned to staff that need completion -->

<template>
  <div class="rounded-lg bg-white p-6 shadow">
    <div class="mb-4 flex items-center justify-between">
      <div>
        <h2 class="text-lg font-semibold text-gray-900">Pending Tasks</h2>
        <p class="mt-1 text-sm text-gray-600">
          {{ pendingTasks.length }} task{{ pendingTasks.length !== 1 ? 's' : '' }} assigned to you
        </p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="py-8 text-center">
      <div class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
      <p class="mt-2 text-sm text-gray-600">Loading pending tasks...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="pendingTasks.length === 0" class="py-8 text-center">
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
          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <p class="mt-2 text-sm text-gray-600">No pending tasks</p>
    </div>

    <!-- Pending Tasks List -->
    <div v-else class="space-y-3">
      <div
        v-for="task in pendingTasks"
        :key="task.id"
        class="cursor-pointer rounded-lg border border-gray-200 p-4 transition hover:border-blue-500 hover:bg-blue-50"
        @click="$emit('complete', task)"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <h3 class="font-medium text-gray-900">{{ task.title }}</h3>
            <div class="mt-2 space-y-1 text-sm text-gray-600">
              <div class="flex items-center">
                <svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
                <span>{{ formatDate(task.activity_date) }}</span>
              </div>
              <div class="flex items-center">
                <svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
                <span>{{ task.customer_name }} - {{ task.location }}</span>
              </div>
              <div v-if="task.task_category" class="flex items-center">
                <span
                  class="inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium"
                  :style="{ backgroundColor: task.task_category.color + '20', color: task.task_category.color }"
                >
                  {{ task.task_category.title }}
                </span>
              </div>
            </div>
          </div>
          <div class="ml-4">
            <span class="inline-flex items-center rounded-full bg-yellow-100 px-2.5 py-0.5 text-xs font-medium text-yellow-800">
              Pending
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';
import type { FieldActivity } from '@/types/field';

defineProps<{
  pendingTasks: FieldActivity[];
  loading: boolean;
}>();

defineEmits<{
  complete: [task: FieldActivity];
}>();

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};
</script>
