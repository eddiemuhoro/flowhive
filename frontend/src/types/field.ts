// Field Operations Type Definitions
// Used exclusively for field team activity tracking

export enum WorkspaceType {
  PROJECT_MANAGEMENT = "PROJECT_MANAGEMENT",
  FIELD_OPERATIONS = "FIELD_OPERATIONS",
}

// Task Category (manager-controlled categories)
export interface TaskCategory {
  id: number;
  name: string;
  title: string;
  description: string | null;
  color: string;
  icon: string | null;
  workspace_id: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCategoryCreate {
  name: string;
  title: string;
  description?: string;
  color: string;
  icon?: string;
  workspace_id: number;
}

export interface TaskCategoryUpdate {
  name?: string;
  title?: string;
  description?: string;
  color?: string;
  icon?: string;
  is_active?: boolean;
}

// Field Activity Photo
export interface FieldActivityPhoto {
  id: number;
  field_activity_id: number;
  file_path: string;
  file_name: string;
  file_size: number;
  mime_type: string;
  uploaded_by: number;
  uploaded_at: string;
}

// Field Activity (core model for field worker logs)
export interface FieldActivity {
  id: number;
  workspace_id: number;
  support_staff_id: number;
  support_staff_name: string;
  title: string;
  activity_date: string; // YYYY-MM-DD
  start_time: string; // HH:MM:SS
  end_time: string; // HH:MM:SS
  customer_name: string;
  location: string;
  task_description: string;
  task_category_id: number | null;
  task_category: TaskCategory | null;
  remarks: string;
  customer_rep: string;
  duration_hours: number;
  created_by: number;
  created_by_name: string;
  updated_by: number | null;
  updated_by_name: string | null;
  created_at: string;
  updated_at: string;
}

export interface FieldActivityCreate {
  workspace_id: number;
  support_staff_id: number;
  title: string;
  activity_date: string;
  start_time: string;
  end_time: string;
  customer_name: string;
  location: string;
  task_description: string;
  task_category_id?: number | null;
  remarks: string;
  customer_rep: string;
}

export interface FieldActivityUpdate {
  support_staff_id?: number;
  title?: string;
  activity_date?: string;
  start_time?: string;
  end_time?: string;
  customer_name?: string;
  location?: string;
  task_description?: string;
  task_category_id?: number;
  remarks?: string;
  customer_rep?: string;
}

export interface FieldActivityDetail extends FieldActivity {
  photos: FieldActivityPhoto[];
}

// Analytics Types
export interface StaffHoursAnalytics {
  staff_id: number;
  staff_name: string;
  total_hours: number;
  activity_count: number;
}

export interface CategoryAnalytics {
  category_id: number | null;
  category_name: string;
  category_title: string;
  activity_count: number;
  total_hours: number;
}

export interface FieldAnalytics {
  total_activities: number;
  total_hours: number;
  hours_by_staff: StaffHoursAnalytics[];
  activities_by_category: CategoryAnalytics[];
  date_range: {
    start: string;
    end: string;
  };
}

// Filter Types
export interface FieldActivityFilters {
  date_from?: string;
  date_to?: string;
  support_staff_id?: number;
  task_category_id?: number;
  customer_name?: string;
}
