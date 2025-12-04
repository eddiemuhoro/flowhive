import { defineStore } from 'pinia'
import { ref } from 'vue'
import { workspaceService, projectService } from '@/services/workspace.service'
import type { Workspace, WorkspaceDetail, Project, ProjectDetail, TaskList } from '@/types/workspace'

export const useWorkspaceStore = defineStore('workspace', () => {
  const workspaces = ref<Workspace[]>([])
  const currentWorkspace = ref<WorkspaceDetail | null>(null)
  const projects = ref<Project[]>([])
  const currentProject = ref<ProjectDetail | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchWorkspaces() {
    try {
      loading.value = true
      error.value = null
      workspaces.value = await workspaceService.getWorkspaces()
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch workspaces'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchWorkspace(id: number) {
    try {
      loading.value = true
      error.value = null
      currentWorkspace.value = await workspaceService.getWorkspace(id)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch workspace'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createWorkspace(data: Partial<Workspace>) {
    try {
      loading.value = true
      error.value = null
      const workspace = await workspaceService.createWorkspace(data)
      workspaces.value.push(workspace)
      return workspace
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create workspace'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateWorkspace(id: number, data: Partial<Workspace>) {
    try {
      loading.value = true
      error.value = null
      const workspace = await workspaceService.updateWorkspace(id, data)
      const index = workspaces.value.findIndex(w => w.id === id)
      if (index !== -1) {
        workspaces.value[index] = workspace
      }
      if (currentWorkspace.value?.id === id) {
        currentWorkspace.value = { ...currentWorkspace.value, ...workspace }
      }
      return workspace
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update workspace'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteWorkspace(id: number) {
    try {
      loading.value = true
      error.value = null
      await workspaceService.deleteWorkspace(id)
      workspaces.value = workspaces.value.filter(w => w.id !== id)
      if (currentWorkspace.value?.id === id) {
        currentWorkspace.value = null
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete workspace'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchProjects(workspaceId: number) {
    try {
      loading.value = true
      error.value = null
      projects.value = await projectService.getWorkspaceProjects(workspaceId)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch projects'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchProject(id: number) {
    try {
      loading.value = true
      error.value = null
      currentProject.value = await projectService.getProject(id)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch project'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createProject(data: Partial<Project>) {
    try {
      loading.value = true
      error.value = null
      const project = await projectService.createProject(data)
      projects.value.push(project)
      return project
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create project'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createTaskList(data: Partial<TaskList>) {
    try {
      loading.value = true
      error.value = null
      const taskList = await projectService.createTaskList(data)
      if (currentProject.value && currentProject.value.id === data.project_id) {
        currentProject.value.task_lists.push(taskList)
      }
      return taskList
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create task list'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    workspaces,
    currentWorkspace,
    projects,
    currentProject,
    loading,
    error,
    fetchWorkspaces,
    fetchWorkspace,
    createWorkspace,
    updateWorkspace,
    deleteWorkspace,
    fetchProjects,
    fetchProject,
    createProject,
    createTaskList
  }
})
