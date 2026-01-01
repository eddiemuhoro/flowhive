export interface Task {
  id: number
  title: string
  description?: string
  project_id: number
  parent_task_id?: number
  creator_id: number
  assignee_id?: number
  status: TaskStatus
  priority: TaskPriority
  due_date?: string
  start_date?: string
  completed_at?: string
  position: number
  estimated_hours?: number
  actual_hours?: number
  created_at: string
  updated_at: string
  assignee_name?: string
  creator_name?: string
}

export enum TaskStatus {
  TODO = 'todo',
  IN_PROGRESS = 'in_progress',
  IN_REVIEW = 'in_review',
  COMPLETED = 'completed',
  BLOCKED = 'blocked'
}

export enum TaskPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent'
}

export interface TaskDetail extends Task {
  subtasks: Subtask[]
  assignee_name?: string
  creator_name?: string
}

export interface Subtask {
  id: number
  title: string
  status: TaskStatus
  priority: TaskPriority
  assignee_id?: number
  due_date?: string
  completed_at?: string
}

export interface Comment {
  id: number
  content: string
  task_id: number
  user_id: number
  parent_comment_id?: number
  created_at: string
  updated_at: string
  user_name?: string
  user_avatar?: string
}

export interface Attachment {
  id: number
  filename: string
  original_filename: string
  file_path: string
  file_size: number
  mime_type: string
  task_id: number
  uploaded_by: number
  uploader_name?: string
  created_at: string
}

export interface ActivityLog {
  id: number
  task_id: number
  user_id: number
  user_name?: string
  action: string
  details?: string
  created_at: string
}
