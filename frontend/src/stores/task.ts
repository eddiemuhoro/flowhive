import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { taskService, commentService, attachmentService } from '@/services/task.service'
import type { Task, TaskDetail, Comment, Attachment, TaskStatus } from '@/types/task'

export const useTaskStore = defineStore('task', () => {
  const tasks = ref<Task[]>([])
  const myTasks = ref<Task[]>([])
  const currentTask = ref<TaskDetail | null>(null)
  const comments = ref<Comment[]>([])
  const attachments = ref<Attachment[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const tasksByStatus = computed(() => {
    const grouped: Record<TaskStatus, Task[]> = {
      todo: [],
      in_progress: [],
      in_review: [],
      completed: [],
      blocked: []
    }

    tasks.value.forEach(task => {
      grouped[task.status].push(task)
    })

    return grouped
  })

  async function fetchTasks(params?: {
    task_list_id?: number
    assignee_id?: number
    status?: string
  }) {
    try {
      loading.value = true
      error.value = null
      tasks.value = await taskService.getTasks(params)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch tasks'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchMyTasks(status?: string) {
    try {
      loading.value = true
      error.value = null
      myTasks.value = await taskService.getMyTasks(status)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch my tasks'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchTask(id: number) {
    try {
      loading.value = true
      error.value = null
      currentTask.value = await taskService.getTask(id)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch task'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createTask(data: Partial<Task>) {
    try {
      loading.value = true
      error.value = null
      const task = await taskService.createTask(data)
      tasks.value.push(task)
      return task
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create task'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateTask(id: number, data: Partial<Task>) {
    try {
      loading.value = true
      error.value = null
      const task = await taskService.updateTask(id, data)

      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value[index] = task
      }

      if (currentTask.value?.id === id) {
        currentTask.value = { ...currentTask.value, ...task }
      }

      return task
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update task'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteTask(id: number) {
    try {
      loading.value = true
      error.value = null
      await taskService.deleteTask(id)
      tasks.value = tasks.value.filter(t => t.id !== id)
      if (currentTask.value?.id === id) {
        currentTask.value = null
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete task'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchComments(taskId: number) {
    try {
      comments.value = await commentService.getTaskComments(taskId)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch comments'
      throw err
    }
  }

  async function addComment(data: Partial<Comment>) {
    try {
      const comment = await commentService.createComment(data)
      comments.value.push(comment)
      return comment
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to add comment'
      throw err
    }
  }

  async function fetchAttachments(taskId: number) {
    try {
      attachments.value = await attachmentService.getTaskAttachments(taskId)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch attachments'
      throw err
    }
  }

  async function uploadAttachment(taskId: number, file: File) {
    try {
      const attachment = await attachmentService.uploadAttachment(taskId, file)
      attachments.value.push(attachment)
      return attachment
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to upload attachment'
      throw err
    }
  }

  return {
    tasks,
    myTasks,
    currentTask,
    comments,
    attachments,
    loading,
    error,
    tasksByStatus,
    fetchTasks,
    fetchMyTasks,
    fetchTask,
    createTask,
    updateTask,
    deleteTask,
    fetchComments,
    addComment,
    fetchAttachments,
    uploadAttachment
  }
})
