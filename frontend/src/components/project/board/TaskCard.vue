<template>
  <div
    :draggable="draggable"
    @dragstart="$emit('dragstart', $event, task)"
    @click="$emit('click', task.id)"
    :class="['p-3 rounded border hover:shadow-md cursor-move transition group', cardClasses]"
  >
    <div class="flex items-start justify-between mb-1">
      <h5 class="font-medium text-gray-900 text-sm flex-1">{{ task.title }}</h5>
      <button
        @click.stop="$emit('edit', task)"
        :class="['opacity-0 group-hover:opacity-100 transition ml-2', editButtonClasses]"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
        </svg>
      </button>
    </div>

    <p v-if="task.description" class="text-xs text-gray-600 line-clamp-2 mb-2">
      {{ task.description }}
    </p>

    <div class="flex items-center justify-between mb-2">
      <select
        v-model="task.priority"
        @click.stop
        @change="$emit('updatePriority', task)"
        :class="['px-2 py-1 text-xs font-medium rounded border-0 cursor-pointer', getPriorityClass(task.priority)]"
      >
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
        <option value="urgent">Urgent</option>
      </select>

      <span v-if="task.assignee_name" class="text-xs text-gray-500">
        {{ task.assignee_name.split(' ')[0] }}
      </span>
    </div>

    <div v-if="task.due_date" :class="['flex items-center text-xs mt-1', getDueDateClass(task.due_date)]">
      <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
      {{ formatDueDate(task.due_date) }}
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Task } from '@/types/task'
import { useTaskFormatting } from '@/composables/useTaskFormatting'

interface Props {
  task: Task
  draggable?: boolean
  cardClasses?: string
  editButtonClasses?: string
}

withDefaults(defineProps<Props>(), {
  draggable: true,
  cardClasses: 'bg-gray-50 border-gray-200 hover:border-primary-300',
  editButtonClasses: 'text-gray-400 hover:text-primary-600'
})

defineEmits<{
  dragstart: [event: DragEvent, task: Task]
  click: [taskId: number]
  edit: [task: Task]
  updatePriority: [task: Task]
}>()

const { formatDueDate, getDueDateClass, getPriorityClass } = useTaskFormatting()
</script>
