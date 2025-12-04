<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Top Navigation -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-2xl font-bold text-primary-600">Flowhive</h1>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <RouterLink
                to="/"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="isActive('/') ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                Dashboard
              </RouterLink>
              <RouterLink
                to="/workspaces"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="isActive('/workspaces') ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                Workspaces
              </RouterLink>
              <RouterLink
                to="/my-tasks"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="isActive('/my-tasks') ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                My Tasks
              </RouterLink>
              <RouterLink
                v-if="authStore.isManager"
                to="/analytics"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="isActive('/analytics') ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                Analytics
              </RouterLink>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <!-- Notifications -->
            <button
              @click="showNotifications = !showNotifications"
              class="relative p-2 text-gray-400 hover:text-gray-500"
            >
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              <span v-if="unreadCount > 0" class="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-500"></span>
            </button>

            <!-- User menu -->
            <div class="flex items-center space-x-3">
              <span class="text-sm font-medium text-gray-700">{{ authStore.user?.full_name || authStore.user?.username }}</span>
              <button
                @click="handleLogout"
                class="text-sm text-gray-500 hover:text-gray-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Notifications Panel -->
    <div
      v-if="showNotifications"
      class="fixed top-16 right-4 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50 max-h-96 overflow-y-auto"
    >
      <div class="p-4 border-b border-gray-200">
        <div class="flex justify-between items-center">
          <h3 class="text-lg font-semibold">Notifications</h3>
          <button @click="notificationStore.markAllAsRead()" class="text-xs text-primary-600 hover:text-primary-800">
            Mark all as read
          </button>
        </div>
      </div>
      <div v-if="notificationStore.notifications.length === 0" class="p-4 text-center text-gray-500">
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
          <p class="text-xs text-gray-400 mt-1">{{ formatDate(notification.timestamp) }}</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notification'
import { format } from 'date-fns'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const showNotifications = ref(false)

const unreadCount = computed(() =>
  notificationStore.notifications.filter(n => !n.read).length
)

const isActive = (path: string) => {
  return route.path === path || route.path.startsWith(path + '/')
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const formatDate = (date: Date) => {
  return format(date, 'MMM d, h:mm a')
}
</script>
