<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Workspace Details</h1>
    <div v-if="workspaceStore.loading" class="text-center py-12">Loading...</div>
    <div v-else-if="workspaceStore.currentWorkspace" class="space-y-6">
      <div class="bg-white shadow rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-2">{{ workspaceStore.currentWorkspace.name }}</h2>
        <p class="text-gray-600">{{ workspaceStore.currentWorkspace.description }}</p>
      </div>

      <!-- Members Section -->
      <div class="bg-white shadow rounded-lg p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">Team Members</h3>
          <button
            v-if="isOwner"
            @click="showAddMember = true"
            class="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            Add Member
          </button>
        </div>
        <div class="space-y-3">
          <div
            v-for="member in workspaceStore.currentWorkspace.members"
            :key="member.user_id"
            class="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            <div class="flex items-center space-x-3">
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-primary-500 flex items-center justify-center text-white font-semibold">
                {{ (member.full_name || member.username).charAt(0).toUpperCase() }}
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900">{{ member.full_name || member.username }}</p>
                <p class="text-xs text-gray-500">{{ member.email }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <span v-if="member.user_id === workspaceStore.currentWorkspace.owner_id" class="px-2 py-1 text-xs font-medium text-primary-700 bg-primary-100 rounded">
                Owner
              </span>
              <button
                v-if="isOwner && member.user_id !== workspaceStore.currentWorkspace.owner_id"
                @click="handleRemoveMember(member.user_id)"
                class="text-red-600 hover:text-red-800 text-sm font-medium"
              >
                Remove
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white shadow rounded-lg p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">Projects</h3>
          <button
            @click="showCreateProject = true"
            class="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            Create Project
          </button>
        </div>
        <div v-if="workspaceStore.projects.length === 0" class="text-center py-8 text-gray-500">
          No projects yet. Create your first project!
        </div>
        <div v-else class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <RouterLink
            v-for="project in workspaceStore.projects"
            :key="project.id"
            :to="`/project/${project.id}`"
            class="border border-gray-200 rounded-lg p-4 hover:border-primary-500 hover:shadow-md transition-all"
          >
            <h4 class="font-medium text-gray-900">{{ project.name }}</h4>
            <p class="text-sm text-gray-500 mt-1">{{ project.description }}</p>
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- Add Member Modal -->
    <div v-if="showAddMember" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="showAddMember = false">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white" @click.stop>
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Add Team Member</h3>
          <div class="space-y-4">
            <div>
              <label for="userSearch" class="block text-sm font-medium text-gray-700 mb-2">Search by email or username</label>
              <input
                id="userSearch"
                v-model="searchQuery"
                @input="handleSearchUsers"
                type="text"
                placeholder="Type to search..."
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              />
            </div>

            <!-- Search Results -->
            <div v-if="searchResults.length > 0" class="border border-gray-200 rounded-md max-h-60 overflow-y-auto">
              <button
                v-for="user in searchResults"
                :key="user.id"
                @click="handleAddMember(user.id)"
                class="w-full text-left px-4 py-3 hover:bg-gray-50 border-b border-gray-100 last:border-b-0"
              >
                <p class="text-sm font-medium text-gray-900">{{ user.full_name || user.username }}</p>
                <p class="text-xs text-gray-500">{{ user.email }}</p>
              </button>
            </div>

            <div v-else-if="searchQuery && !searching" class="text-center py-4 text-gray-500 text-sm">
              No users found
            </div>

            <div v-if="searching" class="text-center py-4 text-gray-500 text-sm">
              Searching...
            </div>
          </div>

          <div class="mt-5 flex justify-end">
            <button
              @click="showAddMember = false"
              class="px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-md border border-gray-300 hover:bg-gray-50"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Project Modal -->
    <div v-if="showCreateProject" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="showCreateProject = false">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white" @click.stop>
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Create New Project</h3>
          <form @submit.prevent="handleCreateProject" class="space-y-4">
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700">Project Name</label>
              <input
                id="name"
                v-model="projectForm.name"
                type="text"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Enter project name"
              />
            </div>
            <div>
              <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                id="description"
                v-model="projectForm.description"
                rows="3"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Enter project description"
              />
            </div>
            <div class="flex justify-end space-x-3 mt-5">
              <button
                type="button"
                @click="showCreateProject = false"
                class="px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-md border border-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="creating"
                class="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
              >
                {{ creating ? 'Creating...' : 'Create' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watchEffect, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useWorkspaceStore } from '@/stores/workspace'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const workspaceStore = useWorkspaceStore()
const authStore = useAuthStore()

const showCreateProject = ref(false)
const showAddMember = ref(false)
const creating = ref(false)
const searching = ref(false)
const searchQuery = ref('')
const searchResults = ref<any[]>([])
let searchTimeout: NodeJS.Timeout | null = null

const projectForm = ref({
  name: '',
  description: '',
  workspace_id: 0
})

const isOwner = computed(() => {
  return workspaceStore.currentWorkspace?.owner_id === authStore.user?.id
})

watchEffect(async () => {
  const id = parseInt(route.params.id as string)
  projectForm.value.workspace_id = id
  await workspaceStore.fetchWorkspace(id)
  await workspaceStore.fetchProjects(id)
})

const handleCreateProject = async () => {
  try {
    creating.value = true
    await workspaceStore.createProject(projectForm.value)
    showCreateProject.value = false
    projectForm.value.name = ''
    projectForm.value.description = ''
    // Refresh projects list
    await workspaceStore.fetchProjects(projectForm.value.workspace_id)
  } catch (error) {
    console.error('Failed to create project:', error)
  } finally {
    creating.value = false
  }
}

const handleSearchUsers = async () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }

  if (!searchQuery.value || searchQuery.value.length < 2) {
    searchResults.value = []
    return
  }

  searchTimeout = setTimeout(async () => {
    try {
      searching.value = true
      const results = await workspaceStore.searchUsers(searchQuery.value)
      // Filter out users who are already members
      const memberIds = workspaceStore.currentWorkspace?.members.map(m => m.user_id) || []
      searchResults.value = results.filter(user => !memberIds.includes(user.id))
    } catch (error) {
      console.error('Failed to search users:', error)
    } finally {
      searching.value = false
    }
  }, 300)
}

const handleAddMember = async (userId: number) => {
  try {
    const workspaceId = parseInt(route.params.id as string)
    await workspaceStore.addMember(workspaceId, userId)
    showAddMember.value = false
    searchQuery.value = ''
    searchResults.value = []
  } catch (error: any) {
    alert(error.response?.data?.detail || 'Failed to add member')
  }
}

const handleRemoveMember = async (userId: number) => {
  if (!confirm('Are you sure you want to remove this member?')) {
    return
  }

  try {
    const workspaceId = parseInt(route.params.id as string)
    await workspaceStore.removeMember(workspaceId, userId)
  } catch (error: any) {
    alert(error.response?.data?.detail || 'Failed to remove member')
  }
}
</script>
