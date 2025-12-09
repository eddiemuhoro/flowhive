<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Task Details</h1>
      <button
        v-if="taskStore.currentTask"
        @click="openEditModal"
        class="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
      >
        Edit Task
      </button>
    </div>
    <div v-if="taskStore.loading" class="text-center py-12">Loading...</div>
    <div v-else-if="taskStore.currentTask" class="space-y-6">
      <div class="bg-white shadow rounded-lg p-6">
        <h2 class="text-2xl font-semibold mb-4">{{ taskStore.currentTask.title }}</h2>
        <p class="text-gray-600 mb-4">{{ taskStore.currentTask.description }}</p>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <span class="text-sm font-medium text-gray-500">Status:</span>
            <span :class="getStatusClass(taskStore.currentTask.status)" class="ml-2 px-2 py-1 text-xs font-medium rounded-full">
              {{ formatStatus(taskStore.currentTask.status) }}
            </span>
          </div>
          <div>
            <span class="text-sm font-medium text-gray-500">Priority:</span>
            <span :class="getPriorityClass(taskStore.currentTask.priority)" class="ml-2 px-2 py-1 text-xs font-medium rounded-full">
              {{ taskStore.currentTask.priority }}
            </span>
          </div>
          <div>
            <span class="text-sm font-medium text-gray-500">Assignee:</span>
            <span class="ml-2 text-sm">{{ taskStore.currentTask.assignee_name || 'Unassigned' }}</span>
          </div>
          <div>
            <span class="text-sm font-medium text-gray-500">Due Date:</span>
            <span class="ml-2 text-sm">{{ taskStore.currentTask.due_date ? new Date(taskStore.currentTask.due_date).toLocaleDateString() : 'Not set' }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white shadow rounded-lg p-6">
        <h3 class="text-lg font-semibold mb-4">Comments</h3>
        <div class="space-y-4">
          <div v-for="comment in taskStore.comments" :key="comment.id" class="border-l-2 border-gray-200 pl-4">
            <div class="flex items-center space-x-2 mb-1">
              <span class="text-sm font-medium">{{ comment.user_name }}</span>
              <span class="text-xs text-gray-500">{{ new Date(comment.created_at).toLocaleDateString() }}</span>
            </div>
            <p class="text-sm text-gray-700">{{ comment.content }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Task Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="showEditModal = false">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white" @click.stop>
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Edit Task</h3>
          <form @submit.prevent="handleUpdateTask" class="space-y-4">
            <div>
              <label for="editTitle" class="block text-sm font-medium text-gray-700">Task Title</label>
              <input
                id="editTitle"
                v-model="editForm.title"
                type="text"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Enter task title"
              />
            </div>
            <div>
              <label for="editDescription" class="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                id="editDescription"
                v-model="editForm.description"
                rows="3"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Enter task description"
              />
            </div>
            <div>
              <label for="editStatus" class="block text-sm font-medium text-gray-700">Status</label>
              <select
                id="editStatus"
                v-model="editForm.status"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                <option value="todo">To Do</option>
                <option value="in_progress">In Progress</option>
                <option value="in_review">In Review</option>
                <option value="completed">Completed</option>
                <option value="blocked">Blocked</option>
              </select>
            </div>
            <div>
              <label for="editPriority" class="block text-sm font-medium text-gray-700">Priority</label>
              <select
                id="editPriority"
                v-model="editForm.priority"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
            <div>
              <label for="editAssignee" class="block text-sm font-medium text-gray-700">Assign To</label>
              <select
                id="editAssignee"
                v-model="editForm.assignee_id"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                <option :value="null">Unassigned</option>
                <option v-for="member in workspaceMembers" :key="member.user_id" :value="member.user_id">
                  {{ member.full_name || member.username }}
                </option>
              </select>
            </div>
            <div>
              <label for="editDueDate" class="block text-sm font-medium text-gray-700">Due Date</label>
              <input
                id="editDueDate"
                v-model="editForm.due_date"
                type="date"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              />
            </div>
            <div class="flex justify-end space-x-3 mt-5">
              <button
                type="button"
                @click="showEditModal = false"
                class="px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-md border border-gray-300 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="updating"
                class="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-md hover:bg-primary-700 disabled:opacity-50"
              >
                {{ updating ? 'Updating...' : 'Update Task' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { TaskStatus, TaskPriority } from '@/types/task'
import { workspaceService } from '@/services/workspace.service'

const route = useRoute()
const taskStore = useTaskStore()

const showEditModal = ref(false)
const updating = ref(false)
const workspaceMembers = ref<any[]>([])
const editForm = ref({
  title: '',
  description: '',
  status: TaskStatus.TODO,
  priority: TaskPriority.MEDIUM,
  assignee_id: null as number | null,
  due_date: ''
})

const getStatusClass = (status: TaskStatus) => {
  const classes = {
    [TaskStatus.TODO]: 'bg-gray-100 text-gray-800',
    [TaskStatus.IN_PROGRESS]: 'bg-blue-100 text-blue-800',
    [TaskStatus.IN_REVIEW]: 'bg-purple-100 text-purple-800',
    [TaskStatus.COMPLETED]: 'bg-green-100 text-green-800',
    [TaskStatus.BLOCKED]: 'bg-red-100 text-red-800'
  }
  return classes[status]
}

const getPriorityClass = (priority: string) => {
  const classes = {
    low: 'bg-gray-100 text-gray-600',
    medium: 'bg-yellow-100 text-yellow-600',
    high: 'bg-orange-100 text-orange-600',
    urgent: 'bg-red-100 text-red-600'
  }
  return classes[priority as keyof typeof classes]
}

const formatStatus = (status: string) => {
  return status.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const openEditModal = async () => {
  if (!taskStore.currentTask) return

  // Populate form with current task data
  editForm.value = {
    title: taskStore.currentTask.title,
    description: taskStore.currentTask.description || '',
    status: taskStore.currentTask.status,
    priority: taskStore.currentTask.priority,
    assignee_id: taskStore.currentTask.assignee_id ?? null,
    due_date: taskStore.currentTask.due_date ? new Date(taskStore.currentTask.due_date).toISOString().split('T')[0] : ''
  }

  // Fetch workspace members if we have workspace_id
  if ((taskStore.currentTask as any).workspace_id && workspaceMembers.value.length === 0) {
    try {
      workspaceMembers.value = await workspaceService.getWorkspaceMembers((taskStore.currentTask as any).workspace_id)
    } catch (error) {
      console.error('Failed to fetch workspace members:', error)
    }
  }

  showEditModal.value = true
}

const handleUpdateTask = async () => {
  if (!taskStore.currentTask) return

  try {
    updating.value = true
    const updateData: any = {
      title: editForm.value.title,
      description: editForm.value.description,
      status: editForm.value.status,
      priority: editForm.value.priority,
      assignee_id: editForm.value.assignee_id ?? undefined
    }

    // Convert date string to ISO datetime if provided
    if (editForm.value.due_date) {
      updateData.due_date = new Date(editForm.value.due_date + 'T00:00:00').toISOString()
    }

    await taskStore.updateTask(taskStore.currentTask.id, updateData)
    await taskStore.fetchTask(taskStore.currentTask.id)
    showEditModal.value = false
  } catch (error) {
    console.error('Failed to update task:', error)
  } finally {
    updating.value = false
  }
}

onMounted(async () => {
  const id = parseInt(route.params.id as string)
  await taskStore.fetchTask(id)
  await taskStore.fetchComments(id)
})
</script>
