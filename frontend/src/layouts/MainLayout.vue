<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <aside
      class="bg-white border-r border-gray-200 flex flex-col transition-all duration-300"
      :class="sidebarCollapsed ? 'w-16' : 'w-64'"
    >
      <!-- Sidebar Header -->
      <div
        class="h-16 flex items-center justify-between px-4 border-b border-gray-200"
      >
        <div v-if="!sidebarCollapsed" class="flex-1 pr-2">
          <WorkspaceSwitcher />
        </div>
        <h1 v-else class="text-xl font-bold text-primary-600">F</h1>
        <button
          @click="sidebarCollapsed = !sidebarCollapsed"
          class="p-1.5 rounded hover:bg-gray-100 text-gray-500 flex-shrink-0"
        >
          <svg
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              :d="
                sidebarCollapsed
                  ? 'M13 5l7 7-7 7M5 5l7 7-7 7'
                  : 'M11 19l-7-7 7-7m8 14l-7-7 7-7'
              "
            />
          </svg>
        </button>
      </div>

      <!-- Sidebar Navigation -->
      <nav class="flex-1 overflow-y-auto py-4">
        <!-- Quick Links -->
        <div class="px-3 mb-4">
          <RouterLink
            to="/"
            class="flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors"
            :class="
              isActive('/') && !isActive('/workspaces')
                ? 'bg-primary-50 text-primary-700'
                : 'text-gray-700 hover:bg-gray-100'
            "
          >
            <svg
              class="w-5 h-5 flex-shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
              />
            </svg>
            <span v-if="!sidebarCollapsed" class="ml-3">Dashboard</span>
          </RouterLink>

          <RouterLink
            to="/my-tasks"
            class="flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors mt-1"
            :class="
              isActive('/my-tasks')
                ? 'bg-primary-50 text-primary-700'
                : 'text-gray-700 hover:bg-gray-100'
            "
          >
            <svg
              class="w-5 h-5 flex-shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
              />
            </svg>
            <span v-if="!sidebarCollapsed" class="ml-3">My Tasks</span>
          </RouterLink>

          <RouterLink
            v-if="authStore.isManager"
            to="/analytics"
            class="flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors mt-1"
            :class="
              isActive('/analytics')
                ? 'bg-primary-50 text-primary-700'
                : 'text-gray-700 hover:bg-gray-100'
            "
          >
            <svg
              class="w-5 h-5 flex-shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
            <span v-if="!sidebarCollapsed" class="ml-3">Analytics</span>
          </RouterLink>
        </div>

        <!-- Workspaces Section -->
        <div v-if="!sidebarCollapsed" class="px-3">
          <div class="flex items-center justify-between px-3 mb-2">
            <h3
              class="text-xs font-semibold text-gray-500 uppercase tracking-wider"
            >
              Workspaces
            </h3>
            <button
              @click="showCreateWorkspace = true"
              class="p-1 rounded hover:bg-gray-100 text-gray-500"
              title="Create workspace"
            >
              <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 4v16m8-8H4"
                />
              </svg>
            </button>
          </div>

          <div
            v-if="workspaceStore.loading"
            class="px-3 py-2 text-xs text-gray-500"
          >
            Loading...
          </div>
          <div
            v-else-if="workspaceStore.workspaces.length === 0"
            class="px-3 py-2 text-xs text-gray-500"
          >
            No workspaces yet
          </div>
          <div v-else class="space-y-1">
            <div
              v-for="workspace in workspaceStore.workspaces"
              :key="workspace.id"
            >
              <!-- Workspace Item -->
              <div
                class="flex items-center justify-between px-3 py-2 rounded-md hover:bg-gray-100 group"
                :class="
                  isActive(`/workspace/${workspace.id}`) ? 'bg-primary-50' : ''
                "
              >
                <button
                  @click="toggleWorkspace(workspace.id)"
                  class="p-1 -ml-1 rounded hover:bg-gray-200 flex-shrink-0"
                  title="Toggle projects"
                >
                  <svg
                    class="w-4 h-4 text-gray-400 transition-transform"
                    :class="
                      expandedWorkspaces.has(workspace.id) ? 'rotate-90' : ''
                    "
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </button>
                <RouterLink
                  :to="`/workspace/${workspace.id}`"
                  class="flex items-center flex-1 min-w-0 ml-1 cursor-pointer"
                  :class="
                    isActive(`/workspace/${workspace.id}`)
                      ? 'text-primary-700 font-semibold'
                      : 'text-gray-700'
                  "
                >
                  <span class="text-sm font-medium truncate">{{
                    workspace.name
                  }}</span>
                </RouterLink>
                <button
                  @click.stop="createProjectInWorkspace(workspace.id)"
                  class="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-gray-200 text-gray-500 flex-shrink-0"
                  title="Add project"
                >
                  <svg
                    class="w-3.5 h-3.5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 4v16m8-8H4"
                    />
                  </svg>
                </button>
              </div>

              <!-- Projects in Workspace -->
              <div
                v-if="expandedWorkspaces.has(workspace.id)"
                class="ml-6 mt-1 space-y-0.5"
              >
                <div
                  v-if="loadingProjects[workspace.id]"
                  class="px-3 py-1 text-xs text-gray-500"
                >
                  Loading projects...
                </div>
                <div
                  v-else-if="workspaceProjects[workspace.id]?.length === 0"
                  class="px-3 py-1 text-xs text-gray-500"
                >
                  No projects
                </div>
                <RouterLink
                  v-else
                  v-for="project in workspaceProjects[workspace.id]"
                  :key="project.id"
                  :to="`/project/${project.id}`"
                  class="flex items-center px-3 py-1.5 rounded-md text-sm transition-colors group"
                  :class="
                    isProjectActive(project.id)
                      ? 'bg-primary-50 text-primary-700'
                      : 'text-gray-600 hover:bg-gray-50'
                  "
                >
                  <div
                    class="w-2 h-2 rounded-full flex-shrink-0"
                    :style="{ backgroundColor: project.color || '#6B7280' }"
                  ></div>
                  <span class="ml-2 truncate">{{ project.name }}</span>
                </RouterLink>
              </div>
            </div>
          </div>
        </div>

        <!-- Collapsed Workspace Icon -->
        <div v-else class="px-3">
          <button
            @click="showWorkspacesList = !showWorkspacesList"
            class="w-full flex items-center justify-center px-3 py-2 rounded-md hover:bg-gray-100"
            title="Workspaces"
          >
            <svg
              class="w-5 h-5 text-gray-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
              />
            </svg>
          </button>
        </div>
      </nav>

      <!-- User Section -->
      <div class="border-t border-gray-200 p-4">
        <div v-if="!sidebarCollapsed" class="flex items-center justify-between">
          <div class="flex items-center min-w-0 flex-1">
            <div
              class="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center flex-shrink-0"
            >
              <span class="text-sm font-medium text-primary-700">
                {{
                  (authStore.user?.full_name ||
                    authStore.user?.username ||
                    "U")[0].toUpperCase()
                }}
              </span>
            </div>
            <div class="ml-3 min-w-0 flex-1">
              <p class="text-sm font-medium text-gray-700 truncate">
                {{ authStore.user?.full_name || authStore.user?.username }}
              </p>
            </div>
          </div>
          <button
            @click="handleLogout"
            class="p-1.5 rounded hover:bg-gray-100 text-gray-500"
            title="Logout"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
              />
            </svg>
          </button>
        </div>
        <div v-else class="flex justify-center">
          <button
            @click="handleLogout"
            class="p-2 rounded hover:bg-gray-100 text-gray-500"
            title="Logout"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
              />
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- Top Bar -->
      <header
        class="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6"
      >
        <div class="flex items-center">
          <!-- Breadcrumb or page title can go here -->
        </div>

        <div class="flex items-center space-x-4">
          <!-- Notifications -->
          <button
            @click="showNotifications = !showNotifications"
            class="relative p-2 text-gray-400 hover:text-gray-500 rounded-full hover:bg-gray-100"
          >
            <svg
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
              />
            </svg>
            <span
              v-if="unreadCount > 0"
              class="absolute top-1 right-1 block h-2 w-2 rounded-full bg-red-500"
            ></span>
          </button>
        </div>
      </header>

      <!-- Notifications Panel -->
      <div
        v-if="showNotifications"
        class="fixed top-16 right-4 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50 max-h-96 overflow-y-auto"
      >
        <div class="p-4 border-b border-gray-200">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-semibold">Notifications</h3>
            <button
              @click="notificationStore.markAllAsRead()"
              class="text-xs text-primary-600 hover:text-primary-800"
            >
              Mark all as read
            </button>
          </div>
        </div>
        <div
          v-if="notificationStore.notifications.length === 0"
          class="p-4 text-center text-gray-500"
        >
          No notifications
        </div>
        <div v-else>
          <div
            v-for="notification in notificationStore.notifications"
            :key="notification.id"
            @click="notificationStore.markAsRead(notification.id)"
            class="p-4 border-b border-gray-100 hover:bg-gray-50 cursor-pointer"
            :class="{ 'bg-blue-50': !notification.read }"
          >
            <p class="font-medium text-sm">{{ notification.title }}</p>
            <p class="text-xs text-gray-600 mt-1">{{ notification.message }}</p>
            <p class="text-xs text-gray-400 mt-1">
              {{ formatDate(notification.timestamp) }}
            </p>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <main class="flex-1 overflow-auto p-6">
        <RouterView />
      </main>
    </div>

    <!-- Create Workspace Modal -->
    > Logout
    <!-- Create Workspace Modal -->
    <div
      v-if="showCreateWorkspace"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="showCreateWorkspace = false"
    >
      <div
        class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white"
        @click.stop
      >
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            Create Workspace
          </h3>
          <form @submit.prevent="handleCreateWorkspace" class="space-y-4">
            <div>
              <label
                for="workspaceName"
                class="block text-sm font-medium text-gray-700"
                >Workspace Name</label
              >
              <input
                id="workspaceName"
                v-model="newWorkspace.name"
                type="text"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="My Workspace"
              />
            </div>
            <div>
              <label
                for="workspaceDescription"
                class="block text-sm font-medium text-gray-700"
                >Description</label
              >
              <textarea
                id="workspaceDescription"
                v-model="newWorkspace.description"
                rows="2"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Optional description"
              />
            </div>
            <div class="flex justify-end space-x-3 mt-5">
              <button
                type="button"
                @click="showCreateWorkspace = false"
                class="px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-md border border-gray-300 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="creatingWorkspace"
                class="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-md hover:bg-primary-700 disabled:opacity-50"
              >
                {{ creatingWorkspace ? "Creating..." : "Create" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Create Project Modal -->
    <div
      v-if="showCreateProject"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="showCreateProject = false"
    >
      <div
        class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white"
        @click.stop
      >
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Create Project</h3>
          <form @submit.prevent="handleCreateProject" class="space-y-4">
            <div>
              <label
                for="projectName"
                class="block text-sm font-medium text-gray-700"
                >Project Name</label
              >
              <input
                id="projectName"
                v-model="newProject.name"
                type="text"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="My Project"
              />
            </div>
            <div>
              <label
                for="projectDescription"
                class="block text-sm font-medium text-gray-700"
                >Description</label
              >
              <textarea
                id="projectDescription"
                v-model="newProject.description"
                rows="2"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Optional description"
              />
            </div>
            <div class="flex justify-end space-x-3 mt-5">
              <button
                type="button"
                @click="showCreateProject = false"
                class="px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-md border border-gray-300 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="creatingProject"
                class="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-md hover:bg-primary-700 disabled:opacity-50"
              >
                {{ creatingProject ? "Creating..." : "Create" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useNotificationStore } from "@/stores/notification";
import { useWorkspaceStore } from "@/stores/workspace";
import { projectService } from "@/services/workspace.service";
import type { Project } from "@/types/workspace";
import { format } from "date-fns";
import WorkspaceSwitcher from "@/components/ui/WorkspaceSwitcher.vue";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const notificationStore = useNotificationStore();
const workspaceStore = useWorkspaceStore();

const showNotifications = ref(false);
const sidebarCollapsed = ref(false);
const expandedWorkspaces = ref<Set<number>>(new Set());
const showWorkspacesList = ref(false);
const workspaceProjects = ref<Record<number, Project[]>>({});
const loadingProjects = ref<Record<number, boolean>>({});

const showCreateWorkspace = ref(false);
const showCreateProject = ref(false);
const creatingWorkspace = ref(false);
const creatingProject = ref(false);
const selectedWorkspaceId = ref<number | null>(null);

const newWorkspace = ref({
  name: "",
  description: "",
});

const newProject = ref({
  name: "",
  description: "",
  workspace_id: 0,
});

const unreadCount = computed(
  () => notificationStore.notifications.filter((n) => !n.read).length,
);

onMounted(async () => {
  await workspaceStore.fetchWorkspaces();

  // Auto-expand workspace if viewing a project
  const projectId = route.params.id;
  if (projectId && route.name === "project") {
    // Find which workspace contains this project
    for (const workspace of workspaceStore.workspaces) {
      await loadWorkspaceProjects(workspace.id);
      const hasProject = workspaceProjects.value[workspace.id]?.some(
        (p) => p.id === parseInt(projectId as string),
      );
      if (hasProject) {
        expandedWorkspaces.value.add(workspace.id);
        break;
      }
    }
  }
});

// Watch route changes to expand relevant workspace
watch(
  () => route.params.id,
  async (newId) => {
    if (newId && route.name === "project") {
      for (const workspace of workspaceStore.workspaces) {
        if (!workspaceProjects.value[workspace.id]) {
          await loadWorkspaceProjects(workspace.id);
        }
        const hasProject = workspaceProjects.value[workspace.id]?.some(
          (p) => p.id === parseInt(newId as string),
        );
        if (hasProject) {
          expandedWorkspaces.value.add(workspace.id);
          break;
        }
      }
    }
  },
);

const isActive = (path: string) => {
  if (path === "/" && route.path === "/") return true;
  if (path === "/" && route.path.startsWith("/workspaces")) return false;
  return route.path.startsWith(path);
};

const isProjectActive = (projectId: number) => {
  return (
    route.name === "project" &&
    parseInt(route.params.id as string) === projectId
  );
};

const toggleWorkspace = async (workspaceId: number) => {
  if (expandedWorkspaces.value.has(workspaceId)) {
    expandedWorkspaces.value.delete(workspaceId);
  } else {
    expandedWorkspaces.value.add(workspaceId);
    if (!workspaceProjects.value[workspaceId]) {
      await loadWorkspaceProjects(workspaceId);
    }
  }
};

const loadWorkspaceProjects = async (workspaceId: number) => {
  if (loadingProjects.value[workspaceId]) return;

  try {
    loadingProjects.value[workspaceId] = true;
    const projects = await projectService.getWorkspaceProjects(workspaceId);
    workspaceProjects.value[workspaceId] = projects;
  } catch (error) {
    console.error("Failed to load projects:", error);
    workspaceProjects.value[workspaceId] = [];
  } finally {
    loadingProjects.value[workspaceId] = false;
  }
};

const createProjectInWorkspace = (workspaceId: number) => {
  selectedWorkspaceId.value = workspaceId;
  newProject.value.workspace_id = workspaceId;
  showCreateProject.value = true;
};

const handleCreateWorkspace = async () => {
  try {
    creatingWorkspace.value = true;
    await workspaceStore.createWorkspace(newWorkspace.value);
    showCreateWorkspace.value = false;
    newWorkspace.value = { name: "", description: "" };
  } catch (error) {
    console.error("Failed to create workspace:", error);
  } finally {
    creatingWorkspace.value = false;
  }
};

const handleCreateProject = async () => {
  try {
    creatingProject.value = true;
    await workspaceStore.createProject(newProject.value);

    // Reload projects for this workspace
    await loadWorkspaceProjects(newProject.value.workspace_id);

    showCreateProject.value = false;
    newProject.value = { name: "", description: "", workspace_id: 0 };
    selectedWorkspaceId.value = null;
  } catch (error) {
    console.error("Failed to create project:", error);
  } finally {
    creatingProject.value = false;
  }
};

const handleLogout = () => {
  authStore.logout();
  router.push("/login");
};

const formatDate = (date: Date) => {
  return format(date, "MMM d, h:mm a");
};
</script>
