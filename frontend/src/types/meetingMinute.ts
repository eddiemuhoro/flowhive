// Meeting Minutes Type Definitions

export interface Attendee {
  id?: number;
  name: string;
}

export interface ActionItem {
  id: number;
  meeting_minute_id: number;
  description: string;
  assigned_to: number | null;
  due_date: string | null;
  status: "pending" | "in_progress" | "completed";
  created_at: string;
  completed_at: string | null;
  assigned_user_name?: string;
}

export interface ActionItemCreate {
  description: string;
  assigned_to?: number | null;
  due_date?: string | null;
  status?: string;
}

export interface ActionItemUpdate {
  description?: string;
  assigned_to?: number | null;
  due_date?: string | null;
  status?: string;
}

export interface MinuteAttachment {
  id: number;
  meeting_minute_id: number;
  cloudinary_public_id: string;
  cloudinary_url: string;
  resource_type: string;
  file_name: string;
  file_size: number;
  mime_type: string;
  uploaded_by: number;
  uploaded_at: string;
  uploader_name?: string;
}

export interface MeetingMinute {
  id: number;
  workspace_id: number;
  title: string;
  meeting_date: string;
  meeting_time_start: string | null;
  meeting_time_end: string | null;
  location: string | null;
  attendees: Attendee[] | null;
  agenda: string | null;
  discussions: string | null;
  decisions: string | null;
  created_by: number;
  created_at: string;
  updated_by: number | null;
  updated_at: string | null;
  created_by_name?: string;
  updated_by_name?: string;
  attachment_count: number;
  action_item_count: number;
}

export interface MeetingMinuteDetail extends MeetingMinute {
  attachments: MinuteAttachment[];
  action_items: ActionItem[];
}

export interface MeetingMinuteCreate {
  workspace_id: number;
  title: string;
  meeting_date: string;
  meeting_time_start?: string | null;
  meeting_time_end?: string | null;
  location?: string | null;
  attendees?: Attendee[] | null;
  agenda?: string | null;
  discussions?: string | null;
  decisions?: string | null;
  action_items?: ActionItemCreate[] | null;
}

export interface MeetingMinuteUpdate {
  title?: string;
  meeting_date?: string;
  meeting_time_start?: string | null;
  meeting_time_end?: string | null;
  location?: string | null;
  attendees?: Attendee[] | null;
  agenda?: string | null;
  discussions?: string | null;
  decisions?: string | null;
}

export interface MeetingMinuteFilters {
  date_from?: string;
  date_to?: string;
  search?: string;
}
