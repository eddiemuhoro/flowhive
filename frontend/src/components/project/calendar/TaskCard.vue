<template>
  <div
    class="border rounded-lg p-3 cursor-pointer hover:shadow-md transition"
    :class="cardColorClass"
  >
    <div class="flex items-start justify-between">
      <div class="flex-1">
        <h5 class="font-medium text-gray-900 text-sm">{{ task.title }}</h5>
        <div class="flex items-center gap-2 mt-1">
          <span class="text-xs px-2 py-0.5 rounded" :class="getStatusClass(task.status)">
            {{ formatStatus(task.status) }}
          </span>
          <span v-if="task.due_date" class="text-xs text-gray-600">{{ formatDueDate(task.due_date) }}</span>
        </div>
      </div>
      <span v-if="task.assignee_name" class="text-xs text-gray-600">
        {{ task.assignee_name.split(' ')[0] }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { type Task } from '@/types/task'
import { useTaskFormatting } from '@/composables/useTaskFormatting'

interface Props {
  task: Task
  colorScheme: 'red' | 'orange' | 'yellow' | 'gray'
}

const props = defineProps<Props>()

const { formatDueDate, getStatusClass, formatStatus } = useTaskFormatting()

const cardColorClass = computed(() => {
  const schemes = {
    red: 'bg-red-50 border-red-200',
    orange: 'bg-orange-50 border-orange-200',
    yellow: 'bg-yellow-50 border-yellow-200',
    gray: 'bg-gray-50 border-gray-200'
  }
  return schemes[props.colorScheme]
})
</script>
