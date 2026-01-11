import { computed, type ComputedRef } from 'vue'
import { isToday, isThisWeek, isPast, parseISO } from 'date-fns'
import type { Task } from '@/types/task'

export function useTaskFilters(tasks: ComputedRef<Task[]>) {
  const getTasksByStatus = (status: string): Task[] => {
    return tasks.value.filter(task => task.status === status)
  }

  const overdueTasks = computed(() => {
    return tasks.value.filter(task => {
      if (!task.due_date || task.status === 'completed') return false
      return isPast(parseISO(task.due_date)) && !isToday(parseISO(task.due_date))
    })
  })

  const todayTasks = computed(() => {
    return tasks.value.filter(task => {
      if (!task.due_date || task.status === 'completed') return false
      return isToday(parseISO(task.due_date))
    })
  })

  const thisWeekTasks = computed(() => {
    return tasks.value.filter(task => {
      if (!task.due_date || task.status === 'completed') return false
      const dueDate = parseISO(task.due_date)
      return isThisWeek(dueDate) && !isToday(dueDate) && !isPast(dueDate)
    })
  })

  const laterTasks = computed(() => {
    return tasks.value.filter(task => {
      if (!task.due_date || task.status === 'completed') return false
      const dueDate = parseISO(task.due_date)
      return !isThisWeek(dueDate) && !isPast(dueDate)
    })
  })

  const noDueDateTasks = computed(() => {
    return tasks.value.filter(task => !task.due_date && task.status !== 'completed')
  })

  return {
    getTasksByStatus,
    overdueTasks,
    todayTasks,
    thisWeekTasks,
    laterTasks,
    noDueDateTasks
  }
}
