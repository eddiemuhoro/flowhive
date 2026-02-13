export interface FieldActivityAnalytics {
  total_activities: number;
  total_hours: number;
  activities_this_week: number;
  activities_this_month: number;
  top_staff: Array<{
    user_id: number;
    name: string;
    activity_count: number;
  }>;
  category_distribution: Record<string, number>;
}

export interface TaskAnalytics {
  total_tasks: number;
  completed_tasks: number;
  in_progress_tasks: number;
  overdue_tasks: number;
  completion_rate: number;
  average_completion_time: number | null;
}

export interface ProjectAnalytics {
  project_id: number;
  project_name: string;
  total_tasks: number;
  completed_tasks: number;
  completion_rate: number;
}

export interface UserProductivity {
  user_id: number;
  user_name: string;
  tasks_assigned: number;
  tasks_completed: number;
  completion_rate: number;
  average_hours_per_task: number | null;
}

export interface WorkspaceAnalytics {
  workspace_id: number;
  workspace_name: string;
  total_projects: number;
  total_tasks: number;
  completed_tasks: number;
  active_members: number;
  completion_rate: number;
  projects: ProjectAnalytics[];
  field_activities?: FieldActivityAnalytics | null;
}

export interface ExecutiveDashboard {
  overview: TaskAnalytics;
  workspaces: WorkspaceAnalytics[];
  top_performers: UserProductivity[];
  task_completion_trend: Array<{
    date: string;
    completed: number;
  }>;
  priority_distribution: Record<string, number>;
  status_distribution: Record<string, number>;
}
