import { apiClient } from './api'
import type { Workspace, WorkspaceDetail, Project, ProjectDetail } from '@/types/workspace'

export const workspaceService = {
  async getWorkspaces(): Promise<Workspace[]> {
    const response = await apiClient.get<Workspace[]>('/workspaces')
    return response.data
  },

  async getWorkspace(id: number): Promise<WorkspaceDetail> {
    const response = await apiClient.get<WorkspaceDetail>(`/workspaces/${id}`)
    return response.data
  },

  async createWorkspace(data: Partial<Workspace>): Promise<Workspace> {
    const response = await apiClient.post<Workspace>('/workspaces', data)
    return response.data
  },

  async updateWorkspace(id: number, data: Partial<Workspace>): Promise<Workspace> {
    const response = await apiClient.patch<Workspace>(`/workspaces/${id}`, data)
    return response.data
  },

  async deleteWorkspace(id: number): Promise<void> {
    await apiClient.delete(`/workspaces/${id}`)
  },

  async addMember(workspaceId: number, userId: number): Promise<void> {
    await apiClient.post(`/workspaces/${workspaceId}/members/${userId}`)
  },

  async removeMember(workspaceId: number, userId: number): Promise<void> {
    await apiClient.delete(`/workspaces/${workspaceId}/members/${userId}`)
  },

  async getWorkspaceMembers(workspaceId: number): Promise<any[]> {
    const response = await apiClient.get(`/workspaces/${workspaceId}/members`)
    return response.data
  }
}

export const projectService = {
  async getWorkspaceProjects(workspaceId: number): Promise<Project[]> {
    const response = await apiClient.get<Project[]>(`/projects/workspace/${workspaceId}`)
    return response.data
  },

  async getProject(id: number): Promise<ProjectDetail> {
    const response = await apiClient.get<ProjectDetail>(`/projects/${id}`)
    return response.data
  },

  async createProject(data: Partial<Project>): Promise<Project> {
    const response = await apiClient.post<Project>('/projects', data)
    return response.data
  },

  async updateProject(id: number, data: Partial<Project>): Promise<Project> {
    const response = await apiClient.patch<Project>(`/projects/${id}`, data)
    return response.data
  },

  async deleteProject(id: number): Promise<void> {
    await apiClient.delete(`/projects/${id}`)
  }
}
