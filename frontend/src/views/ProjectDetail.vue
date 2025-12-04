<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Project Details</h1>
    <div v-if="workspaceStore.loading" class="text-center py-12">Loading...</div>
    <div v-else-if="workspaceStore.currentProject" class="space-y-6">
      <div class="bg-white shadow rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-2">{{ workspaceStore.currentProject.name }}</h2>
        <p class="text-gray-600">{{ workspaceStore.currentProject.description }}</p>
      </div>

      <div class="bg-white shadow rounded-lg p-6">
        <h3 class="text-lg font-semibold mb-4">Task Lists</h3>
        <div class="space-y-4">
          <div
            v-for="taskList in workspaceStore.currentProject.task_lists"
            :key="taskList.id"
            class="border border-gray-200 rounded-lg p-4"
          >
            <h4 class="font-medium text-gray-900">{{ taskList.name }}</h4>
            <p class="text-sm text-gray-500 mt-1">{{ taskList.description }}</p>
          </div>
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
  await workspaceStore.fetchProject(id)
})
</script>
