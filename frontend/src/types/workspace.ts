export interface Workspace {
  id: number
  name: string
  description?: string
  icon?: string
  color?: string
  owner_id: number
  created_at: string
  updated_at: string
}

export interface WorkspaceMember {
  id: number
  user_id: number
  username: string
  email: string
  full_name?: string
  avatar_url?: string
  joined_at: string
}

export interface WorkspaceDetail extends Workspace {
  members: WorkspaceMember[]
}

export interface Project {
  id: number
  name: string
  description?: string
  workspace_id: number
  color?: string
  icon?: string
  created_at: string
  updated_at: string
}

export interface TaskList {
  id: number
  name: string
  description?: string
  project_id: number
  position: number
  created_at: string
  updated_at: string
}

export interface ProjectDetail extends Project {
  task_lists: TaskList[]
}
