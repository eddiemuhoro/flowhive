<template>
  <div class="bg-white shadow rounded-lg">
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Task</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Assignee</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr
            v-for="task in tasks"
            :key="task.id"
            class="hover:bg-gray-50 cursor-pointer transition"
            @click="$emit('taskClick', task.id)"
          >
            <td class="px-6 py-4">
              <div class="text-sm font-medium text-gray-900">{{ task.title }}</div>
              <div v-if="task.description" class="text-sm text-gray-500 line-clamp-1">{{ task.description }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <select
                v-model="task.status"
                @click.stop
                @change="$emit('statusChange', task)"
                class="text-xs font-medium rounded-full px-3 py-1 border-0 cursor-pointer"
                :class="getStatusClass(task.status)"
              >
                <option value="todo">To Do</option>
                <option value="in_progress">In Progress</option>
                <option value="in_review">In Review</option>
                <option value="completed">Completed</option>
                <option value="blocked">Blocked</option>
              </select>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <select
                v-model="task.priority"
                @click.stop
                @change="$emit('priorityChange', task)"
                class="text-xs font-medium rounded px-2 py-1 border-0 cursor-pointer"
                :class="getPriorityClass(task.priority)"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ task.assignee_name || 'Unassigned' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span v-if="task.due_date" class="text-xs" :class="getDueDateClass(task.due_date)">
                {{ formatDueDate(task.due_date) }}
              </span>
              <span v-else class="text-xs text-gray-400">No deadline</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button
                @click.stop="$emit('taskEdit', task)"
                class="text-primary-600 hover:text-primary-900"
              >
                Edit
              </button>
            </td>
          </tr>
          <tr v-if="tasks.length === 0">
            <td colspan="6" class="px-6 py-8 text-center text-gray-500">
              No tasks yet. Create your first task!
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type Task } from '@/types/task'
import { useTaskFormatting } from '@/composables/useTaskFormatting'

interface Props {
  tasks: Task[]
}

defineProps<Props>()

defineEmits<{
  taskClick: [taskId: number]
  taskEdit: [task: Task]
  statusChange: [task: Task]
  priorityChange: [task: Task]
}>()

const { formatDueDate, getDueDateClass, getPriorityClass, getStatusClass } = useTaskFormatting()
</script>
