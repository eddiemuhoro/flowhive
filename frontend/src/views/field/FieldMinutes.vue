<!-- Field Minutes View -->
<!-- Coming Soon page for meeting minutes feature -->

<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <div class="max-w-2xl w-full">
      <!-- Coming Soon Card -->
      <div class="bg-white rounded-2xl shadow-lg p-8 md:p-12 text-center">
        <!-- Icon -->
        <div class="flex justify-center mb-6">
          <div class="bg-blue-100 rounded-full p-6">
            <svg
              class="h-16 w-16 text-blue-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
          </div>
        </div>

        <!-- Content -->
        <h1 class="text-3xl md:text-4xl font-bold text-gray-900 mb-3">
          Meeting Minutes
        </h1>
        <p class="text-xl text-blue-600 font-semibold mb-4">Coming Soon</p>
        <p class="text-gray-600 mb-8 max-w-lg mx-auto">
          We're working on a powerful meeting minutes feature to help you
          document and track important field meetings, decisions, and action
          items.
        </p>

        <!-- Features Preview -->
        <div class="bg-gray-50 rounded-xl p-6 mb-8">
          <h2 class="text-lg font-semibold text-gray-800 mb-4">
            Upcoming Features
          </h2>
          <ul class="space-y-3 text-left max-w-md mx-auto">
            <li class="flex items-start">
              <svg
                class="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 13l4 4L19 7"
                />
              </svg>
              <span class="text-gray-700"
                >Record meeting attendees and location</span
              >
            </li>
            <li class="flex items-start">
              <svg
                class="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 13l4 4L19 7"
                />
              </svg>
              <span class="text-gray-700"
                >Document discussions and decisions</span
              >
            </li>
            <li class="flex items-start">
              <svg
                class="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 13l4 4L19 7"
                />
              </svg>
              <span class="text-gray-700"
                >Track action items and follow-ups</span
              >
            </li>
            <li class="flex items-start">
              <svg
                class="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 13l4 4L19 7"
                />
              </svg>
              <span class="text-gray-700">Share minutes with team members</span>
            </li>
          </ul>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-col sm:flex-row gap-3 justify-center">
          <router-link
            to="/field"
            class="inline-flex items-center justify-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            <svg
              class="h-5 w-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
            Back to Dashboard
          </router-link>
          <router-link
            to="/field/activities"
            class="inline-flex items-center justify-center px-6 py-3 bg-white border-2 border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
          >
            View Activity Log
          </router-link>
        </div>
      </div>

      <!-- Support Info -->
      <div class="mt-6 text-center text-sm text-gray-500">
        <p>Have suggestions for this feature? Contact your administrator.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// No additional logic needed for coming soon page
</script>
