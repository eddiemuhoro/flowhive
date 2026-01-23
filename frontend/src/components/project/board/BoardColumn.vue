<template>
  <div class="flex flex-col">
    <div class="flex items-center justify-between mb-3 pb-2 border-b-2" :class="borderColorClass">
      <h3 class="font-semibold" :class="titleColorClass">{{ title }}</h3>
      <div class="flex items-center gap-2">
        <button
          @click="toggleQuickAdd"
          class="transition"
          :class="addButtonColorClass"
          title="Quick add task"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
        </button>
        <span class="text-sm text-gray-500">{{ tasks.length }}</span>
      </div>
    </div>

    <!-- Quick Add Form -->
    <div v-if="showQuickAdd" class="mb-2 space-y-2">
      <input
        v-model="quickTitle"
        @keyup.enter="handleCreateTask"
        @keyup.esc="handleCancel"
        type="text"
        placeholder="Task title..."
        class="w-full px-3 py-2 text-sm border rounded focus:outline-none focus:ring-2"
        :class="inputColorClass"
        autofocus
      />
      <input
        v-model="quickDueDate"
        @keyup.enter="handleCreateTask"
        @keyup.esc="handleCancel"
        type="date"
        class="w-full px-3 py-2 text-sm border rounded focus:outline-none focus:ring-2"
        :class="inputColorClass"
      />
      <div class="flex gap-2">
        <button
          @click="handleCreateTask"
          class="flex-1 px-3 py-1.5 text-xs font-medium text-white rounded hover:opacity-90 transition"
          :class="buttonBgClass"
        >
          Add Task
        </button>
        <button
          @click="handleCancel"
          class="px-3 py-1.5 text-xs font-medium text-gray-600 bg-gray-100 rounded hover:bg-gray-200 transition"
        >
          Cancel
        </button>
      </div>
    </div>

    <div
      class="space-y-2 flex-1 min-h-[200px]"
      @dragover.prevent
      @drop="handleDrop"
    >
      <div
        v-for="task in tasks"
        :key="task.id"
        draggable="true"
        @dragstart="(e) => $emit('dragstart', e, task)"
        @click="$emit('taskClick', task.id)"
        class="p-3 rounded border hover:shadow-md cursor-move transition group"
        :class="cardColorClass"
      >
        <div class="flex items-start justify-between mb-1">
          <h5 class="font-medium text-gray-900 text-sm flex-1">{{ task.title }}</h5>
          <button
            @click.stop="$emit('taskEdit', task)"
            class="opacity-0 group-hover:opacity-100 text-gray-400 transition ml-2"
            :class="editButtonColorClass"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
            </svg>
          </button>
        </div>
        <p v-if="task.description" class="text-xs text-gray-600 line-clamp-2 mb-2">{{ task.description }}</p>
        <div class="flex items-center justify-between mb-2">
          <select
            v-model="task.priority"
            @click.stop
            @change="$emit('priorityChange', task)"
            class="px-2 py-1 text-xs font-medium rounded border-0 cursor-pointer"
            :class="getPriorityClass(task.priority)"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>
          <span v-if="task.assignee_name" class="text-xs text-gray-500">
            {{ task.assignee_name.split(' ')[task.assignee_name.split(' ').length - 1] }}
          </span>
        </div>
        <div v-if="task.due_date" class="flex items-center text-xs mt-1" :class="getDueDateClass(task.due_date)">
          <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          {{ formatDueDate(task.due_date) }}
        </div>
      </div>
      <div v-if="tasks.length === 0 && !showQuickAdd" class="text-center py-8 text-sm text-gray-400">
        No tasks
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { type Task } from '@/types/task'
import { useTaskFormatting } from '@/composables/useTaskFormatting'

interface Props {
  status: string
  title: string
  tasks: Task[]
  colorScheme: 'gray' | 'blue' | 'purple' | 'green' | 'red'
}

const props = defineProps<Props>()

const emit = defineEmits<{
  createTask: [status: string, title: string, dueDate: string]
  dragstart: [event: DragEvent, task: Task]
  drop: [event: DragEvent, status: string]
  taskClick: [taskId: number]
  taskEdit: [task: Task]
  priorityChange: [task: Task]
}>()

const { formatDueDate, getDueDateClass, getPriorityClass } = useTaskFormatting()

const showQuickAdd = ref(false)
const quickTitle = ref('')
const quickDueDate = ref('')

const toggleQuickAdd = () => {
  showQuickAdd.value = !showQuickAdd.value
}

const handleCreateTask = () => {
  if (quickTitle.value.trim()) {
    emit('createTask', props.status, quickTitle.value.trim(), quickDueDate.value)
    quickTitle.value = ''
    quickDueDate.value = ''
    showQuickAdd.value = false
  }
}

const handleCancel = () => {
  quickTitle.value = ''
  quickDueDate.value = ''
  showQuickAdd.value = false
}

const handleDrop = (event: DragEvent) => {
  emit('drop', event, props.status)
}

// Color scheme computed properties
const colorClasses = computed(() => {
  const schemes = {
    gray: {
      border: 'border-gray-300',
      title: 'text-gray-700',
      addButton: 'text-gray-400 hover:text-gray-600',
      input: 'border-gray-300 focus:ring-primary-500 focus:border-primary-500',
      button: 'bg-primary-600 hover:bg-primary-700',
      card: 'bg-gray-50 border-gray-200 hover:border-primary-300',
      editButton: 'hover:text-primary-600'
    },
    blue: {
      border: 'border-blue-300',
      title: 'text-blue-700',
      addButton: 'text-blue-400 hover:text-blue-600',
      input: 'border-blue-300 focus:ring-blue-500 focus:border-blue-500',
      button: 'bg-blue-600 hover:bg-blue-700',
      card: 'bg-blue-50 border-blue-200 hover:border-blue-400',
      editButton: 'hover:text-blue-600'
    },
    purple: {
      border: 'border-purple-300',
      title: 'text-purple-700',
      addButton: 'text-purple-400 hover:text-purple-600',
      input: 'border-purple-300 focus:ring-purple-500 focus:border-purple-500',
      button: 'bg-purple-600 hover:bg-purple-700',
      card: 'bg-purple-50 border-purple-200 hover:border-purple-400',
      editButton: 'hover:text-purple-600'
    },
    green: {
      border: 'border-green-300',
      title: 'text-green-700',
      addButton: 'text-green-400 hover:text-green-600',
      input: 'border-green-300 focus:ring-green-500 focus:border-green-500',
      button: 'bg-green-600 hover:bg-green-700',
      card: 'bg-green-50 border-green-200 hover:border-green-400',
      editButton: 'hover:text-green-600'
    },
    red: {
      border: 'border-red-300',
      title: 'text-red-700',
      addButton: 'text-red-400 hover:text-red-600',
      input: 'border-red-300 focus:ring-red-500 focus:border-red-500',
      button: 'bg-red-600 hover:bg-red-700',
      card: 'bg-red-50 border-red-200 hover:border-red-400',
      editButton: 'hover:text-red-600'
    }
  }
  return schemes[props.colorScheme]
})

const borderColorClass = computed(() => colorClasses.value.border)
const titleColorClass = computed(() => colorClasses.value.title)
const addButtonColorClass = computed(() => colorClasses.value.addButton)
const inputColorClass = computed(() => colorClasses.value.input)
const buttonBgClass = computed(() => colorClasses.value.button)
const cardColorClass = computed(() => colorClasses.value.card)
const editButtonColorClass = computed(() => colorClasses.value.editButton)
</script>
