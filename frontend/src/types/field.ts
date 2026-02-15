// Field Operations Type Definitions
// Used exclusively for field team activity tracking

export enum WorkspaceType {
  PROJECT_MANAGEMENT = "PROJECT_MANAGEMENT",
  FIELD_OPERATIONS = "FIELD_OPERATIONS",
}

export enum ActivityStatus {
  PENDING = "PENDING",
  IN_PROGRESS = "IN_PROGRESS",
  COMPLETED = "COMPLETED",
}

// Customer (from external SAJSoft API)
export interface Customer {
  id: string;
  clientid: string;
  name: string;
  address: string;
}

// User basic info for creator/updater fields
export interface UserBasicInfo {
  id: number;
  username: string;
  full_name: string | null;
  avatar_url: string | null;
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
  required_role: string;
  is_active: boolean;
  created_by: number | null;
  created_by_user: UserBasicInfo | null;
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
  required_role: string;
}

export interface TaskCategoryUpdate {
  name?: string;
  title?: string;
  description?: string;
  color?: string;
  icon?: string;
  required_role?: string;
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
  start_time: string | null; // HH:MM:SS - null for pending tasks
  end_time: string | null; // HH:MM:SS - null for pending tasks
  customer_id: string | null;
  customer_name: string;
  location: string;
  task_description: string | null; // null for pending tasks
  task_category_id: number | null;
  task_category: TaskCategory | null;
  remarks: string | null;
  customer_rep: string | null;
  status: ActivityStatus;
  duration_hours: number | null; // null for pending tasks
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
  start_time?: string | null; // Optional for PENDING status
  end_time?: string | null; // Optional for PENDING status
  customer_id?: string | null;
  customer_name: string;
  location: string;
  task_description?: string | null; // Optional for PENDING status
  task_category_id?: number | null;
  remarks?: string | null;
  customer_rep?: string | null;
  status?: ActivityStatus; // Defaults to COMPLETED
}

export interface FieldActivityUpdate {
  support_staff_id?: number;
  title?: string;
  activity_date?: string;
  start_time?: string | null;
  end_time?: string | null;
  customer_id?: string | null;
  customer_name?: string;
  location?: string;
  task_description?: string | null;
  task_category_id?: number | null;
  remarks?: string | null;
  customer_rep?: string | null;
  status?: ActivityStatus;
}

export interface FieldActivityDetail extends FieldActivity {
  photos: FieldActivityPhoto[];
}

// Analytics Types
export interface StaffHoursAnalytics {
  user_id: number;
  name: string;
  activity_count: number;
}

export interface CategoryAnalytics {
  category: string;
  count: number;
}

export interface FieldAnalytics {
  total_activities: number;
  hours_by_staff: StaffHoursAnalytics[];
  activities_by_category: CategoryAnalytics[];
}

// Filter Types
export interface FieldActivityFilters {
  date_from?: string;
  date_to?: string;
  support_staff_id?: number;
  task_category_id?: number;
  customer_name?: string;
  search?: string; // Search in task_description field
  status?: ActivityStatus; // Filter by status
}
