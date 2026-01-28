import type { Task } from "./task";

export enum WorkspaceType {
  PROJECT_MANAGEMENT = "PROJECT_MANAGEMENT",
  FIELD_OPERATIONS = "FIELD_OPERATIONS",
}

export interface Workspace {
  id: number;
  name: string;
  description?: string;
  icon?: string;
  color?: string;
  owner_id: number;
  workspace_type: WorkspaceType;
  created_at: string;
  updated_at: string;
}

export interface WorkspaceMember {
  id: number;
  user_id: number;
  username: string;
  email: string;
  role: "owner" | "manager" | "member";
  full_name?: string;
  avatar_url?: string;
  joined_at: string;
}

export interface WorkspaceDetail extends Workspace {
  members: WorkspaceMember[];
}

export interface Project {
  id: number;
  name: string;
  description?: string;
  workspace_id: number;
  color?: string;
  icon?: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectDetail extends Project {
  tasks: Task[];
}
