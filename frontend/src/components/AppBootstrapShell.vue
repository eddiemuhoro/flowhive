<template>
  <div
    class="min-h-screen bg-gray-50 flex animate-pulse"
    role="status"
    aria-live="polite"
  >
    <span class="sr-only">Loading...</span>
    <aside class="hidden md:flex md:w-64 md:flex-col bg-white border-r border-gray-200">
      <div class="h-16 border-b border-gray-200 px-4 flex items-center">
        <div class="h-6 w-32 rounded bg-gray-200"></div>
      </div>
      <div class="p-4 space-y-3">
        <div class="h-4 w-3/4 rounded bg-gray-200"></div>
        <div class="h-4 w-2/3 rounded bg-gray-200"></div>
        <div class="h-4 w-4/5 rounded bg-gray-200"></div>
        <div class="h-4 w-1/2 rounded bg-gray-200"></div>
      </div>
      <div class="mt-auto p-4 border-t border-gray-200">
        <div class="h-8 w-24 rounded bg-gray-200"></div>
      </div>
    </aside>

    <div class="flex-1 flex flex-col">
      <header class="h-16 bg-white border-b border-gray-200 px-6 flex items-center">
        <div class="h-5 w-40 rounded bg-gray-200"></div>
      </header>
      <main class="flex-1 p-6">
        <div class="space-y-4">
          <div class="h-6 w-2/3 rounded bg-gray-200"></div>
          <div class="h-4 w-full rounded bg-gray-200"></div>
          <div class="h-4 w-5/6 rounded bg-gray-200"></div>
          <div class="h-4 w-3/4 rounded bg-gray-200"></div>
        </div>
      </main>
    </div>
  </div>
</template>
