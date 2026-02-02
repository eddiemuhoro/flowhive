import { defineStore } from "pinia";
import { ref } from "vue";
import { workspaceService, projectService } from "@/services/workspace.service";
import type {
  Workspace,
  WorkspaceDetail,
  Project,
  ProjectDetail,
} from "@/types/workspace";

const WORKSPACE_ID_KEY = "flowhive_current_workspace_id";

export const useWorkspaceStore = defineStore("workspace", () => {
  const workspaces = ref<Workspace[]>([]);
  const currentWorkspace = ref<WorkspaceDetail | null>(null);
  const projects = ref<Project[]>([]);
  const currentProject = ref<ProjectDetail | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Helper function to save workspace ID to localStorage
  const saveWorkspaceId = (id: number) => {
    try {
      localStorage.setItem(WORKSPACE_ID_KEY, String(id));
    } catch (err) {
      console.error("Failed to save workspace ID to localStorage:", err);
    }
  };

  // Helper function to get workspace ID from localStorage
  const getSavedWorkspaceId = (): number | null => {
    try {
      const id = localStorage.getItem(WORKSPACE_ID_KEY);
      return id ? Number(id) : null;
    } catch (err) {
      console.error("Failed to get workspace ID from localStorage:", err);
      return null;
    }
  };

  // Helper function to clear saved workspace ID
  const clearSavedWorkspaceId = () => {
    try {
      localStorage.removeItem(WORKSPACE_ID_KEY);
    } catch (err) {
      console.error("Failed to clear workspace ID from localStorage:", err);
    }
  };

  async function fetchWorkspaces() {
    try {
      loading.value = true;
      error.value = null;
      workspaces.value = await workspaceService.getWorkspaces();
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Failed to fetch workspaces";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchWorkspace(id: number) {
    try {
      loading.value = true;
      error.value = null;
      currentWorkspace.value = await workspaceService.getWorkspace(id);
      saveWorkspaceId(id);
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Failed to fetch workspace";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function createWorkspace(data: Partial<Workspace>) {
    try {
      loading.value = true;
      error.value = null;
      const workspace = await workspaceService.createWorkspace(data);
      workspaces.value.push(workspace);
      return workspace;
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Failed to create workspace";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function updateWorkspace(id: number, data: Partial<Workspace>) {
    try {
      loading.value = true;
      error.value = null;
      const workspace = await workspaceService.updateWorkspace(id, data);
      const index = workspaces.value.findIndex((w) => w.id === id);
      if (index !== -1) {
        workspaces.value[index] = workspace;
      }
      if (currentWorkspace.value?.id === id) {
        currentWorkspace.value = { ...currentWorkspace.value, ...workspace };
      }
      return workspace;
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Failed to update workspace";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function deleteWorkspace(id: number) {
    try {
      loading.value = true;
      error.value = null;
      await workspaceService.deleteWorkspace(id);
      workspaces.value = workspaces.value.filter((w) => w.id !== id);
      if (currentWorkspace.value?.id === id) {
        currentWorkspace.value = null;
        clearSavedWorkspaceId();
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Failed to delete workspace";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchProjects(workspaceId: number) {
    try {
      loading.value = true;
      error.value = null;
      projects.value = await projectService.getWorkspaceProjects(workspaceId);
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Failed to fetch projects";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchProject(id: number) {
    try {
      loading.value = true;
      error.value = null;
      currentProject.value = await projectService.getProject(id);
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Failed to fetch project";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function createProject(data: Partial<Project>) {
    try {
      loading.value = true;
      error.value = null;
      const project = await projectService.createProject(data);
      projects.value.push(project);
      return project;
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Failed to create project";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function addMember(workspaceId: number, userId: number) {
    try {
      loading.value = true;
      error.value = null;
      await workspaceService.addMember(workspaceId, userId);
      // Refresh workspace to get updated members list
      await fetchWorkspace(workspaceId);
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Failed to add member";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function removeMember(workspaceId: number, userId: number) {
    try {
      loading.value = true;
      error.value = null;
      await workspaceService.removeMember(workspaceId, userId);
      // Refresh workspace to get updated members list
      await fetchWorkspace(workspaceId);
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Failed to remove member";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function searchUsers(query: string) {
    try {
      return await workspaceService.searchUsers(query);
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Failed to search users";
      throw err;
    }
  }

  /**
   * Initialize workspace from localStorage
   * Should be called on app mount to restore last selected workspace
   * If no workspace is saved, fetch all workspaces and auto-select the first one
   */
  async function initializeWorkspace() {
    const savedId = getSavedWorkspaceId();
    if (savedId && !currentWorkspace.value) {
      try {
        await fetchWorkspace(savedId);
        return true; // Workspace restored from localStorage
      } catch (err) {
        console.error("Failed to restore workspace from localStorage:", err);
        clearSavedWorkspaceId();
      }
    }

    // If no saved workspace, fetch all workspaces and auto-select first one
    if (!currentWorkspace.value) {
      try {
        await fetchWorkspaces();
        if (workspaces.value.length > 0) {
          await fetchWorkspace(workspaces.value[0].id);
          return true; // First workspace auto-selected
        }
      } catch (err) {
        console.error("Failed to auto-select workspace:", err);
      }
    }

    return false; // No workspace available
  }

  /**
   * Clear current workspace (on logout)
   */
  function clearWorkspace() {
    currentWorkspace.value = null;
    clearSavedWorkspaceId();
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
    addMember,
    removeMember,
    searchUsers,
    initializeWorkspace,
    clearWorkspace,
    getSavedWorkspaceId,
  };
});
