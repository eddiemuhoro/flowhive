import { format, isToday, isThisWeek, isPast, parseISO, differenceInDays } from 'date-fns'

export function useTaskFormatting() {
  const formatDueDate = (date: string | undefined) => {
    if (!date) return ''
    const dueDate = parseISO(date)
    const today = new Date()
    const diffDays = differenceInDays(dueDate, today)

    if (isToday(dueDate)) return 'Today'
    if (diffDays === 1) return 'Tomorrow'
    if (diffDays === -1) return 'Yesterday'
    if (diffDays < -1) return format(dueDate, 'MMM d') + ' (overdue)'
    if (diffDays <= 7) return format(dueDate, 'EEE, MMM d')
    return format(dueDate, 'MMM d, yyyy')
  }

  const getDueDateClass = (date: string | undefined) => {
    if (!date) return ''
    const dueDate = parseISO(date)

    if (isPast(dueDate) && !isToday(dueDate)) return 'text-red-600 font-semibold'
    if (isToday(dueDate)) return 'text-orange-600 font-semibold'
    if (isThisWeek(dueDate)) return 'text-yellow-600'
    return 'text-gray-600'
  }

  const getPriorityClass = (priority: string) => {
    const classes = {
      'low': 'bg-yellow-100 text-yellow-800',
      'medium': 'bg-blue-100 text-blue-800',
      'high': 'bg-orange-100 text-orange-800',
      'urgent': 'bg-red-100 text-red-800'
    }
    return classes[priority as keyof typeof classes] || classes.medium
  }

  const getStatusClass = (status: string) => {
    const classes = {
      'todo': 'bg-gray-100 text-gray-800',
      'in_progress': 'bg-blue-100 text-blue-800',
      'in_review': 'bg-purple-100 text-purple-800',
      'completed': 'bg-green-100 text-green-800',
      'blocked': 'bg-red-100 text-red-800'
    }
    return classes[status as keyof typeof classes] || classes.todo
  }

  const formatStatus = (status: string) => {
    return status.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
  }

  return {
    formatDueDate,
    getDueDateClass,
    getPriorityClass,
    getStatusClass,
    formatStatus
  }
}
