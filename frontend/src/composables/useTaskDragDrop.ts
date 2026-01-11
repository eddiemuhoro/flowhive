import { ref, type Ref } from 'vue'
import { useTaskStore } from '@/stores/task'
import { useWorkspaceStore } from '@/stores/workspace'
import { TaskStatus, type Task } from '@/types/task'

export function useTaskDragDrop(projectId: Ref<number>) {
  const taskStore = useTaskStore()
  const workspaceStore = useWorkspaceStore()
  const draggedTask = ref<Task | null>(null)

  const handleDragStart = (event: DragEvent, task: Task) => {
    draggedTask.value = task
    if (event.dataTransfer) {
      event.dataTransfer.effectAllowed = 'move'
    }
  }

  const handleDrop = async (event: DragEvent, newStatus: string) => {
    event.preventDefault()

    if (!draggedTask.value || draggedTask.value.status === newStatus) {
      draggedTask.value = null
      return
    }

    try {
      await taskStore.updateTask(draggedTask.value.id, { status: newStatus as TaskStatus })
      await workspaceStore.fetchProject(projectId.value)
    } catch (error) {
      console.error('Failed to update task status:', error)
    } finally {
      draggedTask.value = null
    }
  }

  return {
    draggedTask,
    handleDragStart,
    handleDrop
  }
}
