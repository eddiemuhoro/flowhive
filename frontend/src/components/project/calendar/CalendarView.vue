<template>
  <div class="bg-white shadow rounded-lg p-6">
    <div class="mb-4 flex items-center justify-between">
      <h3 class="text-lg font-semibold text-gray-900">Tasks by Due Date</h3>
    </div>

    <div class="space-y-4">
      <!-- Overdue Tasks -->
      <div v-if="overdueTasks.length > 0" class="border-l-4 border-red-500 pl-4">
        <h4 class="text-sm font-semibold text-red-700 mb-2 flex items-center">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Overdue ({{ overdueTasks.length }})
        </h4>
        <div class="space-y-2">
          <TaskCard
            v-for="task in overdueTasks"
            :key="task.id"
            :task="task"
            color-scheme="red"
            @click="$emit('taskClick', task.id)"
          />
        </div>
      </div>

      <!-- Due Today -->
      <div v-if="todayTasks.length > 0" class="border-l-4 border-orange-500 pl-4">
        <h4 class="text-sm font-semibold text-orange-700 mb-2">Due Today ({{ todayTasks.length }})</h4>
        <div class="space-y-2">
          <TaskCard
            v-for="task in todayTasks"
            :key="task.id"
            :task="task"
            color-scheme="orange"
            @click="$emit('taskClick', task.id)"
          />
        </div>
      </div>

      <!-- Due This Week -->
      <div v-if="thisWeekTasks.length > 0" class="border-l-4 border-yellow-500 pl-4">
        <h4 class="text-sm font-semibold text-yellow-700 mb-2">Due This Week ({{ thisWeekTasks.length }})</h4>
        <div class="space-y-2">
          <TaskCard
            v-for="task in thisWeekTasks"
            :key="task.id"
            :task="task"
            color-scheme="yellow"
            @click="$emit('taskClick', task.id)"
          />
        </div>
      </div>

      <!-- Later -->
      <div v-if="laterTasks.length > 0" class="border-l-4 border-gray-300 pl-4">
        <h4 class="text-sm font-semibold text-gray-700 mb-2">Later ({{ laterTasks.length }})</h4>
        <div class="space-y-2">
          <TaskCard
            v-for="task in laterTasks"
            :key="task.id"
            :task="task"
            color-scheme="gray"
            @click="$emit('taskClick', task.id)"
          />
        </div>
      </div>

      <!-- No Due Date -->
      <div v-if="noDueDateTasks.length > 0" class="border-l-4 border-gray-200 pl-4">
        <h4 class="text-sm font-semibold text-gray-500 mb-2">No Due Date ({{ noDueDateTasks.length }})</h4>
        <div class="space-y-2">
          <TaskCard
            v-for="task in noDueDateTasks"
            :key="task.id"
            :task="task"
            color-scheme="gray"
            @click="$emit('taskClick', task.id)"
          />
        </div>
      </div>

      <div v-if="allTasks.length === 0" class="text-center py-12 text-gray-500">
        No tasks yet. Create your first task!
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type Task } from '@/types/task'
import TaskCard from './TaskCard.vue'

interface Props {
  allTasks: Task[]
  overdueTasks: Task[]
  todayTasks: Task[]
  thisWeekTasks: Task[]
  laterTasks: Task[]
  noDueDateTasks: Task[]
}

defineProps<Props>()

defineEmits<{
  taskClick: [taskId: number]
}>()
</script>
