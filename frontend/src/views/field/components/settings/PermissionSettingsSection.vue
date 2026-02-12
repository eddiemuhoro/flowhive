<!-- Permission Settings Section Component -->
<template>
  <div class="rounded-lg bg-white p-6 shadow-sm">
    <h2 class="text-lg font-semibold text-gray-900 mb-4">
      Permission Settings
    </h2>
    <p class="text-sm text-gray-600 mb-4">
      Define what each user role can do in the system
    </p>

    <div class="space-y-4">
      <!-- Team Member Permissions -->
      <div class="rounded-lg border border-gray-200 p-4">
        <div class="mb-3 flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <div class="rounded bg-gray-100 px-2 py-1">
              <span class="text-sm font-semibold text-gray-700">Team Member</span>
            </div>
            <span class="text-sm text-gray-500">(Default Role)</span>
          </div>
        </div>
        <ul class="space-y-2 text-sm text-gray-600">
          <li class="flex items-center space-x-2">
            <svg class="h-4 w-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <span>Create and edit own field activities</span>
          </li>
          <li class="flex items-center space-x-2">
            <svg class="h-4 w-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <span>View own activities and assigned tasks</span>
          </li>
          <li class="flex items-center space-x-2">
            <svg class="h-4 w-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
            <span>Cannot manage categories or settings</span>
          </li>
          <li class="flex items-center space-x-2">
            <svg class="h-4 w-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
            <span>Cannot add/remove team members</span>
          </li>
        </ul>
      </div>

      <!-- Manager Permissions -->
      <div class="rounded-lg border border-green-200 bg-green-50/50 p-4">
        <div class="mb-3 flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <div class="rounded bg-green-100 px-2 py-1">
              <span class="text-sm font-semibold text-green-700">Manager</span>
            </div>
            <span class="text-sm text-green-600">+ All Team Member permissions</span>
          </div>
        </div>
        <ul class="space-y-2 text-sm text-gray-700">
          <li class="flex items-center space-x-2">
            <svg class="h-4 w-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <span>View all field activities in workspace</span>
          </li>
          <li class="flex items-center space-x-2">
            <svg class="h-4 w-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <span>Manage task categories (create, edit, deactivate)</span>
          </li>
          <li class="flex items-center space-x-2">
            <svg class="h-4 w-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <span>Add and remove team members</span>
          </li>
          <li class="flex items-center space-x-2">
            <svg class="h-4 w-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <span>Access settings and configuration</span>
          </li>
        </ul>
      </div>

      <!-- Executive Permissions -->
      <div class="rounded-lg border border-purple-200 bg-purple-50/50 p-4">
        <div class="mb-3 flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <div class="rounded bg-purple-100 px-2 py-1">
              <span class="text-sm font-semibold text-purple-700">Executive</span>
            </div>
            <span class="text-sm text-purple-600">+ All Manager permissions</span>
          </div>
        </div>
        <ul class="space-y-2 text-sm text-gray-700">
          <li class="flex items-center space-x-2">
            <svg class="h-4 w-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <span>Full control over all workspaces</span>
          </li>
          <li class="flex items-center space-x-2">
            <svg class="h-4 w-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <span>Delete any activities or workspaces</span>
          </li>
          <li class="flex items-center space-x-2">
            <svg class="h-4 w-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <span>Access executive dashboard and analytics</span>
          </li>
          <li class="flex items-center space-x-2">
            <svg class="h-4 w-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <span>Manage all user accounts and roles</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// This is a presentational component with no logic
</script>
