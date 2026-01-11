<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Project Details</h1>
    <div v-if="workspaceStore.loading" class="text-center py-12">Loading...</div>
    <div v-else-if="workspaceStore.currentProject" class="space-y-6">
      <div class="bg-white shadow rounded-lg p-6">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl font-semibold mb-2">{{ workspaceStore.currentProject.name }}</h2>
            <p class="text-gray-600">{{ workspaceStore.currentProject.description }}</p>
          </div>
          <div class="flex items-center gap-3">
            <!-- View Switcher -->
            <div class="flex items-center bg-gray-100 rounded-md p-1">
              <button
                @click="currentView = 'board'"
                class="px-3 py-1.5 text-sm font-medium rounded transition-colors"
                :class="currentView === 'board' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-600 hover:text-gray-900'"
                title="Board View"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </button>
              <button
                @click="currentView = 'list'"
                class="px-3 py-1.5 text-sm font-medium rounded transition-colors"
                :class="currentView === 'list' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-600 hover:text-gray-900'"
                title="List View"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                </svg>
              </button>
              <button
                @click="currentView = 'calendar'"
                class="px-3 py-1.5 text-sm font-medium rounded transition-colors"
                :class="currentView === 'calendar' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-600 hover:text-gray-900'"
                title="Calendar View"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </button>
            </div>
            <button
              @click="openCreateTask()"
              class="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              + Create Task
            </button>
          </div>
        </div>
      </div>

      <!-- Board View -->
      <div v-if="currentView === 'board'" class="bg-white shadow rounded-lg p-6">
        <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
          <BoardColumn
            status="todo"
            title="To Do"
            :tasks="getTasksByStatus('todo')"
            color-scheme="gray"
            @create-task="createQuickTask"
            @dragstart="handleDragStart"
            @drop="handleDrop"
            @task-click="openTaskDetail"
            @task-edit="editTaskInline"
            @priority-change="updateTaskPriority"
          />

          <BoardColumn
            status="in_progress"
            title="In Progress"
            :tasks="getTasksByStatus('in_progress')"
            color-scheme="blue"
            @create-task="createQuickTask"
            @dragstart="handleDragStart"
            @drop="handleDrop"
            @task-click="openTaskDetail"
            @task-edit="editTaskInline"
            @priority-change="updateTaskPriority"
          />

          <BoardColumn
            status="in_review"
            title="In Review"
            :tasks="getTasksByStatus('in_review')"
            color-scheme="purple"
            @create-task="createQuickTask"
            @dragstart="handleDragStart"
            @drop="handleDrop"
            @task-click="openTaskDetail"
            @task-edit="editTaskInline"
            @priority-change="updateTaskPriority"
          />

          <BoardColumn
            status="completed"
            title="Completed"
            :tasks="getTasksByStatus('completed')"
            color-scheme="green"
            @create-task="createQuickTask"
            @dragstart="handleDragStart"
            @drop="handleDrop"
            @task-click="openTaskDetail"
            @task-edit="editTaskInline"
            @priority-change="updateTaskPriority"
          />

          <BoardColumn
            status="blocked"
            title="Blocked"
            :tasks="getTasksByStatus('blocked')"
            color-scheme="red"
            @create-task="createQuickTask"
            @dragstart="handleDragStart"
            @drop="handleDrop"
            @task-click="openTaskDetail"
            @task-edit="editTaskInline"
            @priority-change="updateTaskPriority"
          />
        </div>
      </div>

      <!-- List View -->
      <ListView
        v-if="currentView === 'list'"
        :tasks="allTasks"
        @task-click="openTaskDetail"
        @task-edit="editTaskInline"
        @status-change="updateTaskStatus"
        @priority-change="updateTaskPriority"
      />

      <!-- Calendar View -->
      <CalendarView
        v-if="currentView === 'calendar'"
        :all-tasks="allTasks"
        :overdue-tasks="overdueTasks"
        :today-tasks="todayTasks"
        :this-week-tasks="thisWeekTasks"
        :later-tasks="laterTasks"
        :no-due-date-tasks="noDueDateTasks"
        @task-click="openTaskDetail"
      />
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
              <label for="dueDate" class="block text-sm font-medium text-gray-700">Due Date</label>
              <input
                id="dueDate"
                v-model="taskForm.due_date"
                type="date"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useWorkspaceStore } from '@/stores/workspace'
import { useTaskStore } from '@/stores/task'
import { useAuthStore } from '@/stores/auth'
import { TaskStatus, TaskPriority, type Task } from '@/types/task'
import { workspaceService } from '@/services/workspace.service'
// Import composables for cleaner code organization
import { useTaskFilters } from '@/composables/useTaskFilters'
import { useTaskDragDrop } from '@/composables/useTaskDragDrop'
// Import components to eliminate duplication
import BoardColumn from '@/components/project/board/BoardColumn.vue'
import ListView from '@/components/project/list/ListView.vue'
import CalendarView from '@/components/project/calendar/CalendarView.vue'

const route = useRoute()
const router = useRouter()
const workspaceStore = useWorkspaceStore()
const taskStore = useTaskStore()
const authStore = useAuthStore()

// View state
const currentView = ref<'board' | 'list' | 'calendar'>('board')

const showCreateTask = ref(false)
const creatingTask = ref(false)
const workspaceMembers = ref<any[]>([])
const projectId = ref(0)
const taskForm = ref({
  title: '',
  description: '',
  project_id: 0,
  assignee_id: null as number | null,
  priority: TaskPriority.MEDIUM,
  status: TaskStatus.TODO,
  due_date: '' as string | null
})

// Computed properties for different views
const allTasks = computed(() => {
  return workspaceStore.currentProject?.tasks || []
})

// Use composables for cleaner code organization
const { getTasksByStatus, overdueTasks, todayTasks, thisWeekTasks, laterTasks, noDueDateTasks } = useTaskFilters(allTasks)

// Use drag and drop composable
const { handleDragStart, handleDrop } = useTaskDragDrop(projectId)

// Load project data helper function
const loadProjectData = async (id: number) => {
  projectId.value = id
  taskForm.value.project_id = id
  await workspaceStore.fetchProject(id)

  // Fetch workspace members for assignee dropdown
  if (workspaceStore.currentProject?.workspace_id) {
    try {
      workspaceMembers.value = await workspaceService.getWorkspaceMembers(workspaceStore.currentProject.workspace_id)
    } catch (error) {
      console.error('Failed to fetch workspace members:', error)
    }
  }
}

onMounted(async () => {
  const id = parseInt(route.params.id as string)
  await loadProjectData(id)
})

// Watch for route parameter changes to reload project data when switching between projects
watch(() => route.params.id, async (newId) => {
  if (newId && route.name === 'project') {
    const id = parseInt(newId as string)
    await loadProjectData(id)
  }
})

// Task operations
const updateTaskStatus = async (task: Task) => {
  const oldStatus = task.status
  try {
    // Optimistic update - UI already updated via v-model
    await taskStore.updateTask(task.id, { status: task.status as TaskStatus })
  } catch (error) {
    console.error('Failed to update task status:', error)
    // Revert on error
    task.status = oldStatus
    await workspaceStore.fetchProject(projectId.value)
  }
}

// Quick task creation - now receives parameters from BoardColumn
const createQuickTask = async (status: string, title: string, dueDate: string) => {
  try {
    await taskStore.createTask({
      title,
      project_id: projectId.value,
      status: status as TaskStatus,
      priority: TaskPriority.MEDIUM,
      assignee_id: authStore.user?.id,
      due_date: dueDate ? `${dueDate}T23:59:59` : undefined
    })

    // Refresh project
    await workspaceStore.fetchProject(projectId.value)
  } catch (error) {
    console.error('Failed to create task:', error)
  }
}

// Inline priority update
const updateTaskPriority = async (task: Task) => {
  const oldPriority = task.priority
  try {
    // Optimistic update - UI already updated via v-model
    await taskStore.updateTask(task.id, { priority: task.priority })
  } catch (error) {
    console.error('Failed to update task priority:', error)
    // Revert on error
    task.priority = oldPriority
    await workspaceStore.fetchProject(projectId.value)
  }
}

// Navigate to task detail
const openTaskDetail = (taskId: number) => {
  router.push({ name: 'task', params: { id: taskId } })
}

// Inline editing (opens detail page for now, can be enhanced later)
const editTaskInline = (task: Task) => {
  router.push({ name: 'task', params: { id: task.id } })
}

const openCreateTask = () => {
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
      assignee_id: taskForm.value.assignee_id ?? undefined,
      due_date: taskForm.value.due_date ? `${taskForm.value.due_date}T23:59:59` : undefined
    }
    await taskStore.createTask(taskData)
    showCreateTask.value = false
    taskForm.value.title = ''
    taskForm.value.description = ''
    taskForm.value.assignee_id = null
    taskForm.value.priority = TaskPriority.MEDIUM
    taskForm.value.status = TaskStatus.TODO
    taskForm.value.due_date = ''
    // Refresh project to show new task
    await workspaceStore.fetchProject(projectId.value)
  } catch (error) {
    console.error('Failed to create task:', error)
  } finally {
    creatingTask.value = false
  }
}
</script>
