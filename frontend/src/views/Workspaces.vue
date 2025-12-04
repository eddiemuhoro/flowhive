<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Workspaces</h1>
      <button
        @click="showCreateModal = true"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
      >
        Create Workspace
      </button>
    </div>

    <div v-if="workspaceStore.loading" class="text-center py-12">Loading...</div>

    <div v-else-if="workspaceStore.workspaces.length === 0" class="text-center py-12 bg-white rounded-lg shadow">
      <p class="text-gray-500 mb-4">No workspaces yet</p>
      <button
        @click="showCreateModal = true"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
      >
        Create your first workspace
      </button>
    </div>

    <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <RouterLink
        v-for="workspace in workspaceStore.workspaces"
        :key="workspace.id"
        :to="`/workspace/${workspace.id}`"
        class="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-center">
            <div
              class="flex-shrink-0 h-12 w-12 rounded-lg flex items-center justify-center text-white text-xl font-bold"
              :style="{ backgroundColor: workspace.color || '#0ea5e9' }"
            >
              {{ workspace.icon || workspace.name.charAt(0).toUpperCase() }}
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">{{ workspace.name }}</h3>
              <p class="text-sm text-gray-500">{{ workspace.description }}</p>
            </div>
          </div>
        </div>
      </RouterLink>
    </div>

    <!-- Create Workspace Modal -->
    <div v-if="showCreateModal" class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen px-4">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="showCreateModal = false"></div>

        <div class="bg-white rounded-lg overflow-hidden shadow-xl transform transition-all sm:max-w-lg sm:w-full z-20">
          <form @submit.prevent="handleCreate">
            <div class="px-6 py-4">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Create Workspace</h3>

              <div class="space-y-4">
                <div>
                  <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
                  <input
                    v-model="formData.name"
                    type="text"
                    id="name"
                    required
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  />
                </div>

                <div>
                  <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
                  <textarea
                    v-model="formData.description"
                    id="description"
                    rows="3"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  ></textarea>
                </div>
              </div>
            </div>

            <div class="px-6 py-3 bg-gray-50 flex justify-end space-x-3">
              <button
                type="button"
                @click="showCreateModal = false"
                class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="workspaceStore.loading"
                class="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
              >
                Create
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useWorkspaceStore } from '@/stores/workspace'

const workspaceStore = useWorkspaceStore()
const showCreateModal = ref(false)
const formData = ref({
  name: '',
  description: ''
})

const handleCreate = async () => {
  try {
    await workspaceStore.createWorkspace(formData.value)
    showCreateModal.value = false
    formData.value = { name: '', description: '' }
  } catch (error) {
    console.error('Failed to create workspace:', error)
  }
}

onMounted(() => {
  workspaceStore.fetchWorkspaces()
})
</script>
