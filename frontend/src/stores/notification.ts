import { defineStore } from 'pinia'
import { ref } from 'vue'
import { wsService } from '@/services/websocket.service'

export interface Notification {
  id: string
  type: string
  title: string
  message: string
  timestamp: Date
  read: boolean
}

export const useNotificationStore = defineStore('notification', () => {
  const notifications = ref<Notification[]>([])
  const connected = ref(false)

  function connectWebSocket(workspaceId: number) {
    wsService.connect(workspaceId)
    connected.value = true

    // Listen for various events
    wsService.on('task_created', handleTaskCreated)
    wsService.on('task_updated', handleTaskUpdated)
    wsService.on('task_deleted', handleTaskDeleted)
    wsService.on('comment_added', handleCommentAdded)
    wsService.on('task_assigned', handleTaskAssigned)
  }

  function disconnectWebSocket() {
    wsService.disconnect()
    connected.value = false
  }

  function handleTaskCreated(data: any) {
    addNotification({
      type: 'task_created',
      title: 'New Task Created',
      message: `${data.title} has been created`,
    })
  }

  function handleTaskUpdated(data: any) {
    addNotification({
      type: 'task_updated',
      title: 'Task Updated',
      message: `${data.title} has been updated`,
    })
  }

  function handleTaskDeleted() {
    addNotification({
      type: 'task_deleted',
      title: 'Task Deleted',
      message: `A task has been deleted`,
    })
  }

  function handleCommentAdded(data: any) {
    addNotification({
      type: 'comment_added',
      title: 'New Comment',
      message: `${data.user_name} commented on a task`,
    })
  }

  function handleTaskAssigned(data: any) {
    addNotification({
      type: 'task_assigned',
      title: 'Task Assigned',
      message: `You have been assigned to ${data.title}`,
    })
  }

  function addNotification(notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) {
    notifications.value.unshift({
      ...notification,
      id: Date.now().toString(),
      timestamp: new Date(),
      read: false
    })

    // Keep only last 50 notifications
    if (notifications.value.length > 50) {
      notifications.value = notifications.value.slice(0, 50)
    }
  }

  function markAsRead(id: string) {
    const notification = notifications.value.find(n => n.id === id)
    if (notification) {
      notification.read = true
    }
  }

  function markAllAsRead() {
    notifications.value.forEach(n => n.read = true)
  }

  function clearNotifications() {
    notifications.value = []
  }

  return {
    notifications,
    connected,
    connectWebSocket,
    disconnectWebSocket,
    addNotification,
    markAsRead,
    markAllAsRead,
    clearNotifications
  }
})
