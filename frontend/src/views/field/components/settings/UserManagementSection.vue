<!-- User Management Section Component - Executive Only -->
<template>
  <div v-if="currentUserRole === 'executive'" class="rounded-lg bg-white p-6 shadow-sm">
    <div class="mb-4 flex items-center justify-between">
      <div>
        <h2 class="text-lg font-semibold text-gray-900">User Management</h2>
        <p class="text-sm text-gray-600 mt-1">
          Manage user accounts, roles, and permissions
        </p>
      </div>
      <button
        @click="showAddMember = true"
        class="flex items-center space-x-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
      >
        <svg
          class="h-5 w-5"
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
        <span>Add Member</span>
      </button>
    </div>

    <!-- Users Table -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
              User
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
              Email
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
              Role
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
              Status
            </th>
            <th class="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 bg-white">
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
            <td class="whitespace-nowrap px-4 py-3">
              <div class="flex items-center">
                <div class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-blue-500 text-xs font-semibold text-white">
                  {{ (user.full_name || user.username).charAt(0).toUpperCase() }}
                </div>
                <div class="ml-3">
                  <div class="text-sm font-medium text-gray-900">
                    {{ user.full_name || user.username }}
                  </div>
                  <div class="text-xs text-gray-500">@{{ user.username }}</div>
                </div>
              </div>
            </td>
            <td class="whitespace-nowrap px-4 py-3">
              <div class="text-sm text-gray-900">{{ user.email }}</div>
            </td>
            <td class="whitespace-nowrap px-4 py-3">
              <span
                :class="{
                  'bg-purple-100 text-purple-700': user.role === 'executive',
                  'bg-green-100 text-green-700': user.role === 'manager',
                  'bg-gray-100 text-gray-700': user.role === 'team_member'
                }"
                class="inline-flex rounded-full px-2 py-1 text-xs font-semibold capitalize leading-5"
              >
                {{ user.role?.replace('_', ' ') || 'N/A' }}
              </span>
            </td>
            <td class="whitespace-nowrap px-4 py-3">
              <span
                :class="user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                class="inline-flex rounded-full px-2 py-1 text-xs font-semibold leading-5"
              >
                {{ user.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="whitespace-nowrap px-4 py-3 text-right text-sm font-medium">
              <button
                @click="openEditModal(user)"
                class="mr-3 text-blue-600 hover:text-blue-900"
              >
                Edit
              </button>
              <button
                v-if="user.id !== currentUserId"
                @click="handleDeleteUser(user)"
                class="text-red-600 hover:text-red-900"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="py-8 text-center">
      <div class="text-sm text-gray-500">Loading users...</div>
    </div>

    <!-- Empty State -->
    <div v-else-if="users.length === 0" class="py-8 text-center">
      <div class="text-sm text-gray-500">No users found</div>
    </div>

    <!-- Add Member Modal -->
    <Teleport to="body">
      <div
        v-if="showAddMember"
        class="fixed inset-0 z-50 overflow-y-auto bg-black/50 p-4"
        @click.self="showAddMember = false"
      >
        <div class="mx-auto max-w-lg rounded-lg bg-white p-6 shadow-xl">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-semibold text-gray-900">Add Team Member</h2>
            <button
              @click="showAddMember = false"
              class="rounded-lg p-2 text-gray-400 hover:bg-gray-100"
            >
              <svg
                class="h-5 w-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          <div class="space-y-4">
            <div>
              <label
                for="userSearch"
                class="mb-2 block text-sm font-medium text-gray-700"
              >
                Search by email or username
              </label>
              <input
                id="userSearch"
                v-model="searchQuery"
                @input="handleSearchUsers"
                type="text"
                placeholder="Type to search..."
                class="block w-full rounded-lg border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none sm:text-sm"
              />
            </div>

            <!-- Search Results -->
            <div
              v-if="searchResults.length > 0"
              class="max-h-60 overflow-y-auto rounded-lg border border-gray-200"
            >
              <button
                v-for="user in searchResults"
                :key="user.id"
                @click="handleAddMember(user.id)"
                class="w-full border-b border-gray-100 px-4 py-3 text-left hover:bg-gray-50 last:border-b-0"
              >
                <p class="text-sm font-medium text-gray-900">
                  {{ user.full_name || user.username }}
                </p>
                <p class="text-xs text-gray-500">{{ user.email }}</p>
              </button>
            </div>

            <div
              v-else-if="searchQuery && !searching"
              class="py-4 text-center text-sm text-gray-500"
            >
              No users found
            </div>

            <div
              v-if="searching"
              class="py-4 text-center text-sm text-gray-500"
            >
              Searching...
            </div>
          </div>

          <div class="mt-5 flex justify-end">
            <button
              @click="showAddMember = false"
              class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Edit User Modal -->
    <Teleport to="body">
      <div
        v-if="showEditModal"
        class="fixed inset-0 z-50 overflow-y-auto bg-black/50 p-4"
        @click.self="closeEditModal"
      >
        <div class="mx-auto max-w-lg rounded-lg bg-white p-6 shadow-xl">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-semibold text-gray-900">Edit User</h2>
            <button
              @click="closeEditModal"
              class="rounded-lg p-2 text-gray-400 hover:bg-gray-100"
            >
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="handleUpdateUser" class="space-y-4">
            <!-- Full Name -->
            <div>
              <label class="block text-sm font-medium text-gray-700">Full Name</label>
              <input
                v-model="editForm.full_name"
                type="text"
                class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none"
              />
            </div>

            <!-- Email -->
            <div>
              <label class="block text-sm font-medium text-gray-700">Email</label>
              <input
                v-model="editForm.email"
                type="email"
                required
                class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none"
              />
            </div>

            <!-- Username -->
            <div>
              <label class="block text-sm font-medium text-gray-700">Username</label>
              <input
                v-model="editForm.username"
                type="text"
                required
                class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none"
              />
            </div>

            <!-- Role -->
            <div>
              <label class="block text-sm font-medium text-gray-700">Role</label>
              <select
                v-model="editForm.role"
                class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none"
              >
                <option value="team_member">Team Member</option>
                <option value="manager">Manager</option>
                <option value="executive">Executive</option>
              </select>
            </div>

            <!-- Active Status -->
            <div class="flex items-center">
              <input
                v-model="editForm.is_active"
                type="checkbox"
                id="is_active"
                class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <label for="is_active" class="ml-2 block text-sm text-gray-700">
                Active Account
              </label>
            </div>

            <div class="mt-5 flex justify-end space-x-3">
              <button
                type="button"
                @click="closeEditModal"
                class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="saving"
                class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
              >
                {{ saving ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { userService, type UserUpdateData } from '@/services/user.service'
import type { User } from '@/types/auth'
import type { WorkspaceDetail } from '@/types/workspace'

interface Props {
  workspace: WorkspaceDetail | null
  currentUserId: number | undefined
  currentUserRole: string | undefined
}

const props = defineProps<Props>()

const loading = ref(false)
const saving = ref(false)
const showEditModal = ref(false)
const showAddMember = ref(false)
const editingUser = ref<User | null>(null)
const searchQuery = ref('')
const searchResults = ref<any[]>([])
const searching = ref(false)
let searchTimeout: NodeJS.Timeout | null = null

const editForm = ref<UserUpdateData>({
  email: '',
  username: '',
  full_name: '',
  role: 'team_member',
  is_active: true
})

// Use workspace members as users list
const users = computed(() => {
  if (!props.workspace?.members) return []
  return props.workspace.members.map(member => ({
    id: member.user_id,
    email: member.email,
    username: member.username,
    full_name: member.full_name || '',
    avatar_url: member.avatar_url,
    role: member.system_role as any,
    is_active: true,
    created_at: member.joined_at,
    updated_at: member.joined_at
  }))
})

function openEditModal(user: User) {
  editingUser.value = user
  editForm.value = {
    email: user.email,
    username: user.username,
    full_name: user.full_name || '',
    role: user.role,
    is_active: user.is_active
  }
  showEditModal.value = true
}

function closeEditModal() {
  showEditModal.value = false
  editingUser.value = null
  editForm.value = {
    email: '',
    username: '',
    full_name: '',
    role: 'team_member',
    is_active: true
  }
}

async function handleUpdateUser() {
  if (!editingUser.value || !props.workspace) return

  try {
    saving.value = true
    await userService.updateUser(editingUser.value.id, editForm.value)
    // Refresh workspace data to get updated user info
    const { useWorkspaceStore } = await import('@/stores/workspace')
    const workspaceStore = useWorkspaceStore()
    await workspaceStore.fetchWorkspace(props.workspace.id)
    closeEditModal()
    alert('User updated successfully!')
  } catch (error: any) {
    console.error('Failed to update user:', error)
    alert(error.response?.data?.detail || 'Failed to update user')
  } finally {
    saving.value = false
  }
}

async function handleDeleteUser(user: User) {
  if (!confirm(`Are you sure you want to delete ${user.full_name || user.username}? This action cannot be undone.`)) {
    return
  }

  try {
    await userService.deleteUser(user.id)
    // Refresh workspace data to update members list
    if (props.workspace) {
      const { useWorkspaceStore } = await import('@/stores/workspace')
      const workspaceStore = useWorkspaceStore()
      await workspaceStore.fetchWorkspace(props.workspace.id)
    }
    alert('User deleted successfully!')
  } catch (error: any) {
    console.error('Failed to delete user:', error)
    alert(error.response?.data?.detail || 'Failed to delete user')
  }
}

async function handleSearchUsers() {
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
      const { useWorkspaceStore } = await import('@/stores/workspace')
      const workspaceStore = useWorkspaceStore()
      const results = await workspaceStore.searchUsers(searchQuery.value)
      const memberIds = props.workspace?.members.map((m) => m.user_id) || []
      searchResults.value = results.filter(
        (user) => !memberIds.includes(user.id),
      )
    } catch (error) {
      console.error('Failed to search users:', error)
    } finally {
      searching.value = false
    }
  }, 300)
}

async function handleAddMember(userId: number) {
  if (!props.workspace?.id) return

  try {
    const { useWorkspaceStore } = await import('@/stores/workspace')
    const workspaceStore = useWorkspaceStore()
    await workspaceStore.addMember(props.workspace.id, userId)
    showAddMember.value = false
    searchQuery.value = ''
    searchResults.value = []
    alert('Member added successfully!')
  } catch (error: any) {
    console.error('Failed to add member:', error)
    alert(
      error.response?.data?.detail || 'Failed to add member. Please try again.',
    )
  }
}
</script>
