<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Project Details</h1>
    <div v-if="workspaceStore.loading" class="text-center py-12">Loading...</div>
    <div v-else-if="workspaceStore.currentProject" class="space-y-6">
      <div class="bg-white shadow rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-2">{{ workspaceStore.currentProject.name }}</h2>
        <p class="text-gray-600">{{ workspaceStore.currentProject.description }}</p>
      </div>

      <div class="bg-white shadow rounded-lg p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">Task Lists</h3>
          <button
            @click="showCreateTaskList = true"
            class="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            Create Task List
          </button>
        </div>
        <div v-if="!workspaceStore.currentProject.task_lists || workspaceStore.currentProject.task_lists.length === 0" class="text-center py-8 text-gray-500">
          No task lists yet. Create your first task list!
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="taskList in workspaceStore.currentProject.task_lists"
            :key="taskList.id"
            class="border border-gray-200 rounded-lg p-4"
          >
            <div class="flex items-center justify-between mb-3">
              <div>
                <h4 class="font-medium text-gray-900">{{ taskList.name }}</h4>
                <p class="text-sm text-gray-500 mt-1">{{ taskList.description }}</p>
              </div>
              <button
                @click="openCreateTask(taskList.id)"
                class="px-3 py-1 bg-primary-100 text-primary-700 text-sm font-medium rounded hover:bg-primary-200"
              >
                + Add Task
              </button>
            </div>

            <!-- Tasks in this list -->
            <div v-if="(taskList as any).tasks && (taskList as any).tasks.length > 0" class="mt-4 space-y-2">
              <div
                v-for="task in (taskList as any).tasks"
                :key="task.id"
                @click="$router.push({ name: 'TaskDetail', params: { id: task.id } })"
                class="bg-gray-50 p-3 rounded border border-gray-200 hover:border-primary-300 hover:bg-white cursor-pointer transition"
              >
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <h5 class="font-medium text-gray-900">{{ task.title }}</h5>
                    <p v-if="task.description" class="text-sm text-gray-600 mt-1">{{ task.description }}</p>
                    <div v-if="task.assignee_name" class="flex items-center mt-2">
                      <svg class="w-4 h-4 text-gray-400 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      <span class="text-xs text-gray-500">{{ task.assignee_name }}</span>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2 ml-3">
                    <span
                      class="px-2 py-1 text-xs font-medium rounded"
                      :class="{
                        'bg-yellow-100 text-yellow-800': task.priority === 'low',
                        'bg-blue-100 text-blue-800': task.priority === 'medium',
                        'bg-orange-100 text-orange-800': task.priority === 'high',
                        'bg-red-100 text-red-800': task.priority === 'urgent'
                      }"
                    >
                      {{ task.priority }}
                    </span>
                    <span
                      class="px-2 py-1 text-xs font-medium rounded"
                      :class="{
                        'bg-gray-100 text-gray-800': task.status === 'todo',
                        'bg-blue-100 text-blue-800': task.status === 'in_progress',
                        'bg-purple-100 text-purple-800': task.status === 'in_review',
                        'bg-green-100 text-green-800': task.status === 'completed',
                        'bg-red-100 text-red-800': task.status === 'blocked'
                      }"
                    >
                      {{ task.status.replace('_', ' ') }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="mt-4 text-center py-4 text-sm text-gray-400 border border-dashed border-gray-300 rounded">
              No tasks yet. Click "+ Add Task" to create one.
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Task List Modal -->
    <div v-if="showCreateTaskList" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="showCreateTaskList = false">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white" @click.stop>
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Create Task List</h3>
          <form @submit.prevent="handleCreateTaskList" class="space-y-4">
            <div>
              <label for="taskListName" class="block text-sm font-medium text-gray-700">List Name</label>
              <input
                id="taskListName"
                v-model="taskListForm.name"
                type="text"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="e.g., To Do, In Progress, Done"
              />
            </div>
            <div>
              <label for="taskListDescription" class="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                id="taskListDescription"
                v-model="taskListForm.description"
                rows="2"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Optional description"
              />
            </div>
            <div class="flex justify-end space-x-3 mt-5">
              <button
                type="button"
                @click="showCreateTaskList = false"
                class="px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-md border border-gray-300 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="creatingTaskList"
                class="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-md hover:bg-primary-700 disabled:opacity-50"
              >
                {{ creatingTaskList ? 'Creating...' : 'Create' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Create Task Modal -->
    <div v-if="showCreateTask" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="showCreateTask = false">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white" @click.stop>
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Create Task</h3>
          <form @submit.prevent="handleCreateTask" class="space-y-4">
            <div>
              <label for="taskTitle" class="block text-sm font-medium text-gray-700">Task Title</label>
              <input
                id="taskTitle"
                v-model="taskForm.title"
                type="text"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Enter task title"
              />
            </div>
            <div>
              <label for="taskDescription" class="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                id="taskDescription"
                v-model="taskForm.description"
                rows="3"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Enter task description"
              />
            </div>
            <div>
              <label for="priority" class="block text-sm font-medium text-gray-700">Priority</label>
              <select
                id="priority"
                v-model="taskForm.priority"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
            <div>
              <label for="assignee" class="block text-sm font-medium text-gray-700">Assign To</label>
              <select
                id="assignee"
                v-model="taskForm.assignee_id"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                <option :value="null">Unassigned</option>
                <option v-for="member in workspaceMembers" :key="member.user_id" :value="member.user_id">
                  {{ member.full_name || member.username }}
                </option>
              </select>
            </div>
            <div class="flex justify-end space-x-3 mt-5">
              <button
                type="button"
                @click="showCreateTask = false"
                class="px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-md border border-gray-300 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="creatingTask"
                class="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-md hover:bg-primary-700 disabled:opacity-50"
              >
                {{ creatingTask ? 'Creating...' : 'Create' }}
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
import { useWorkspaceStore } from '@/stores/workspace'
import { useTaskStore } from '@/stores/task'
import { useAuthStore } from '@/stores/auth'
import { TaskStatus, TaskPriority } from '@/types/task'
import { workspaceService } from '@/services/workspace.service'

const route = useRoute()
const workspaceStore = useWorkspaceStore()
const taskStore = useTaskStore()
const authStore = useAuthStore()

const showCreateTaskList = ref(false)
const creatingTaskList = ref(false)
const taskListForm = ref({
  name: '',
  description: '',
  project_id: 0
})

const showCreateTask = ref(false)
const creatingTask = ref(false)
const workspaceMembers = ref<any[]>([])
const taskForm = ref({
  title: '',
  description: '',
  task_list_id: 0,
  assignee_id: null as number | null,
  priority: TaskPriority.MEDIUM,
  status: TaskStatus.TODO
})

onMounted(async () => {
  const id = parseInt(route.params.id as string)
  taskListForm.value.project_id = id
  await workspaceStore.fetchProject(id)

  // Fetch workspace members for assignee dropdown
  if (workspaceStore.currentProject?.workspace_id) {
    try {
      workspaceMembers.value = await workspaceService.getWorkspaceMembers(workspaceStore.currentProject.workspace_id)
    } catch (error) {
      console.error('Failed to fetch workspace members:', error)
    }
  }
})

const handleCreateTaskList = async () => {
  try {
    creatingTaskList.value = true
    await workspaceStore.createTaskList(taskListForm.value)
    showCreateTaskList.value = false
    taskListForm.value.name = ''
    taskListForm.value.description = ''
    // Refresh project to get updated task lists
    await workspaceStore.fetchProject(taskListForm.value.project_id)
  } catch (error) {
    console.error('Failed to create task list:', error)
  } finally {
    creatingTaskList.value = false
  }
}

const openCreateTask = (taskListId: number) => {
  taskForm.value.task_list_id = taskListId
  // Set current user as default assignee
  taskForm.value.assignee_id = authStore.user?.id ?? null
  showCreateTask.value = true
}

const handleCreateTask = async () => {
  try {
    creatingTask.value = true
    // Convert null to undefined for API compatibility
    const taskData = {
      ...taskForm.value,
      assignee_id: taskForm.value.assignee_id ?? undefined
    }
    await taskStore.createTask(taskData)
    showCreateTask.value = false
    taskForm.value.title = ''
    taskForm.value.description = ''
    taskForm.value.assignee_id = null
    taskForm.value.priority = TaskPriority.MEDIUM
    // Refresh project to show new task
    await workspaceStore.fetchProject(taskListForm.value.project_id)
  } catch (error) {
    console.error('Failed to create task:', error)
  } finally {
    creatingTask.value = false
  }
}
</script>
