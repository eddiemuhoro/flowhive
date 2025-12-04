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
        <h3 class="text-lg font-semibold mb-4">Projects</h3>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
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
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useWorkspaceStore } from '@/stores/workspace'

const route = useRoute()
const workspaceStore = useWorkspaceStore()

onMounted(async () => {
  const id = parseInt(route.params.id as string)
  await workspaceStore.fetchWorkspace(id)
  await workspaceStore.fetchProjects(id)
})
</script>
