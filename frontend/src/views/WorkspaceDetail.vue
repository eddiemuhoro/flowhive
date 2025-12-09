<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Workspace Details</h1>
    <div v-if="workspaceStore.loading" class="text-center py-12">Loading...</div>
    <div v-else-if="workspaceStore.currentWorkspace" class="space-y-6">
      <div class="bg-white shadow rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-2">{{ workspaceStore.currentWorkspace.name }}</h2>
        <p class="text-gray-600">{{ workspaceStore.currentWorkspace.description }}</p>
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
import { ref, watchEffect } from 'vue'
import { useRoute } from 'vue-router'
import { useWorkspaceStore } from '@/stores/workspace'

const route = useRoute()
const workspaceStore = useWorkspaceStore()

const showCreateProject = ref(false)
const creating = ref(false)
const projectForm = ref({
  name: '',
  description: '',
  workspace_id: 0
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
</script>
