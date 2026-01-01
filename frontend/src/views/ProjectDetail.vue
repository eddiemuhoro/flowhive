<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Project Details</h1>
    <div v-if="workspaceStore.loading" class="text-center py-12">Loading...</div>
    <div v-else-if="workspaceStore.currentProject" class="space-y-6">
      <div class="bg-white shadow rounded-lg p-6">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl font-semibold mb-2">{{ workspaceStore.currentProject.name }}</h2>
            <p class="text-gray-600">{{ workspaceStore.currentProject.description }}</p>
          </div>
          <div class="flex items-center gap-3">
            <!-- View Switcher -->
            <div class="flex items-center bg-gray-100 rounded-md p-1">
              <button
                @click="currentView = 'board'"
                class="px-3 py-1.5 text-sm font-medium rounded transition-colors"
                :class="currentView === 'board' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-600 hover:text-gray-900'"
                title="Board View"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </button>
              <button
                @click="currentView = 'list'"
                class="px-3 py-1.5 text-sm font-medium rounded transition-colors"
                :class="currentView === 'list' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-600 hover:text-gray-900'"
                title="List View"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                </svg>
              </button>
              <button
                @click="currentView = 'calendar'"
                class="px-3 py-1.5 text-sm font-medium rounded transition-colors"
                :class="currentView === 'calendar' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-600 hover:text-gray-900'"
                title="Calendar View"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </button>
            </div>
            <button
              @click="openCreateTask()"
              class="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              + Create Task
            </button>
          </div>
        </div>
      </div>

      <!-- Board View -->
      <div v-if="currentView === 'board'" class="bg-white shadow rounded-lg p-6">
        <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
          <!-- To Do Column -->
          <div class="flex flex-col">
            <div class="flex items-center justify-between mb-3 pb-2 border-b-2 border-gray-300">
              <h3 class="font-semibold text-gray-700">To Do</h3>
              <div class="flex items-center gap-2">
                <button
                  @click="showQuickAdd.todo = !showQuickAdd.todo"
                  class="text-gray-400 hover:text-gray-600 transition"
                  title="Quick add task"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                </button>
                <span class="text-sm text-gray-500">{{ getTasksByStatus('todo').length }}</span>
              </div>
            </div>

            <!-- Quick Add Form -->
            <div v-if="showQuickAdd.todo" class="mb-2">
              <input
                v-model="quickTaskTitle.todo"
                @keyup.enter="createQuickTask('todo')"
                @keyup.esc="showQuickAdd.todo = false"
                type="text"
                placeholder="Task title... (Enter to save, Esc to cancel)"
                class="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                autofocus
              />
            </div>

            <div
              class="space-y-2 flex-1 min-h-[200px]"
              @dragover.prevent
              @drop="handleDrop($event, 'todo')"
            >
              <div
                v-for="task in getTasksByStatus('todo')"
                :key="task.id"
                draggable="true"
                @dragstart="handleDragStart($event, task)"
                @click="openTaskDetail(task.id)"
                class="bg-gray-50 p-3 rounded border border-gray-200 hover:border-primary-300 hover:shadow-md cursor-move transition group"
              >
                <div class="flex items-start justify-between mb-1">
                  <h5 class="font-medium text-gray-900 text-sm flex-1">{{ task.title }}</h5>
                  <button
                    @click.stop="editTaskInline(task)"
                    class="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-primary-600 transition ml-2"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                  </button>
                </div>
                <p v-if="task.description" class="text-xs text-gray-600 line-clamp-2 mb-2">{{ task.description }}</p>
                <div class="flex items-center justify-between mb-2">
                  <select
                    v-model="task.priority"
                    @click.stop
                    @change="updateTaskPriority(task)"
                    class="px-2 py-1 text-xs font-medium rounded border-0 cursor-pointer"
                    :class="getPriorityClass(task.priority)"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                  <span v-if="task.assignee_name" class="text-xs text-gray-500">
                    {{ task.assignee_name.split(' ')[0] }}
                  </span>
                </div>
                <div v-if="task.due_date" class="flex items-center text-xs mt-1" :class="getDueDateClass(task.due_date)">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  {{ formatDueDate(task.due_date) }}
                </div>
              </div>
              <div v-if="getTasksByStatus('todo').length === 0 && !showQuickAdd.todo" class="text-center py-8 text-sm text-gray-400">
                No tasks
              </div>
            </div>
          </div>

          <!-- In Progress Column -->
          <div class="flex flex-col">
            <div class="flex items-center justify-between mb-3 pb-2 border-b-2 border-blue-300">
              <h3 class="font-semibold text-blue-700">In Progress</h3>
              <div class="flex items-center gap-2">
                <button
                  @click="showQuickAdd.in_progress = !showQuickAdd.in_progress"
                  class="text-blue-400 hover:text-blue-600 transition"
                  title="Quick add task"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                </button>
                <span class="text-sm text-gray-500">{{ getTasksByStatus('in_progress').length }}</span>
              </div>
            </div>

            <!-- Quick Add Form -->
            <div v-if="showQuickAdd.in_progress" class="mb-2">
              <input
                v-model="quickTaskTitle.in_progress"
                @keyup.enter="createQuickTask('in_progress')"
                @keyup.esc="showQuickAdd.in_progress = false"
                type="text"
                placeholder="Task title... (Enter to save)"
                class="w-full px-3 py-2 text-sm border border-blue-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                autofocus
              />
            </div>

            <div
              class="space-y-2 flex-1 min-h-[200px]"
              @dragover.prevent
              @drop="handleDrop($event, 'in_progress')"
            >
              <div
                v-for="task in getTasksByStatus('in_progress')"
                :key="task.id"
                draggable="true"
                @dragstart="handleDragStart($event, task)"
                @click="openTaskDetail(task.id)"
                class="bg-blue-50 p-3 rounded border border-blue-200 hover:border-blue-400 hover:shadow-md cursor-move transition group"
              >
                <div class="flex items-start justify-between mb-1">
                  <h5 class="font-medium text-gray-900 text-sm flex-1">{{ task.title }}</h5>
                  <button
                    @click.stop="editTaskInline(task)"
                    class="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-blue-600 transition ml-2"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                  </button>
                </div>
                <p v-if="task.description" class="text-xs text-gray-600 line-clamp-2 mb-2">{{ task.description }}</p>
                <div v-if="task.due_date" class="flex items-center text-xs mt-1" :class="getDueDateClass(task.due_date)">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  {{ formatDueDate(task.due_date) }}
                </div>
                <div class="flex items-center justify-between mt-2">
                  <select
                    v-model="task.priority"
                    @click.stop
                    @change="updateTaskPriority(task)"
                    class="px-2 py-1 text-xs font-medium rounded border-0 cursor-pointer"
                    :class="getPriorityClass(task.priority)"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                  <span v-if="task.assignee_name" class="text-xs text-gray-500">
                    {{ task.assignee_name.split(' ')[0] }}
                  </span>
                </div>
              </div>
              <div v-if="getTasksByStatus('in_progress').length === 0 && !showQuickAdd.in_progress" class="text-center py-8 text-sm text-gray-400">
                No tasks
              </div>
            </div>
          </div>

          <!-- In Review Column -->
          <div class="flex flex-col">
            <div class="flex items-center justify-between mb-3 pb-2 border-b-2 border-purple-300">
              <h3 class="font-semibold text-purple-700">In Review</h3>
              <div class="flex items-center gap-2">
                <button
                  @click="showQuickAdd.in_review = !showQuickAdd.in_review"
                  class="text-purple-400 hover:text-purple-600 transition"
                  title="Quick add task"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                </button>
                <span class="text-sm text-gray-500">{{ getTasksByStatus('in_review').length }}</span>
              </div>
            </div>

            <!-- Quick Add Form -->
            <div v-if="showQuickAdd.in_review" class="mb-2">
              <input
                v-model="quickTaskTitle.in_review"
                @keyup.enter="createQuickTask('in_review')"
                @keyup.esc="showQuickAdd.in_review = false"
                type="text"
                placeholder="Task title... (Enter to save)"
                class="w-full px-3 py-2 text-sm border border-purple-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                autofocus
              />
            </div>

            <div
              class="space-y-2 flex-1 min-h-[200px]"
              @dragover.prevent
              @drop="handleDrop($event, 'in_review')"
            >
              <div
                v-for="task in getTasksByStatus('in_review')"
                :key="task.id"
                draggable="true"
                @dragstart="handleDragStart($event, task)"
                @click="openTaskDetail(task.id)"
                class="bg-purple-50 p-3 rounded border border-purple-200 hover:border-purple-400 hover:shadow-md cursor-move transition group"
              >
                <div class="flex items-start justify-between mb-1">
                  <h5 class="font-medium text-gray-900 text-sm flex-1">{{ task.title }}</h5>
                  <button
                    @click.stop="editTaskInline(task)"
                    class="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-purple-600 transition ml-2"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                  </button>
                </div>
                <p v-if="task.description" class="text-xs text-gray-600 line-clamp-2 mb-2">{{ task.description }}</p>
                <div v-if="task.due_date" class="flex items-center text-xs mt-1" :class="getDueDateClass(task.due_date)">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  {{ formatDueDate(task.due_date) }}
                </div>
                <div class="flex items-center justify-between mt-2">
                  <select
                    v-model="task.priority"
                    @click.stop
                    @change="updateTaskPriority(task)"
                    class="px-2 py-1 text-xs font-medium rounded border-0 cursor-pointer"
                    :class="getPriorityClass(task.priority)"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                  <span v-if="task.assignee_name" class="text-xs text-gray-500">
                    {{ task.assignee_name.split(' ')[0] }}
                  </span>
                </div>
              </div>
              <div v-if="getTasksByStatus('in_review').length === 0 && !showQuickAdd.in_review" class="text-center py-8 text-sm text-gray-400">
                No tasks
              </div>
            </div>
          </div>

          <!-- Completed Column -->
          <div class="flex flex-col">
            <div class="flex items-center justify-between mb-3 pb-2 border-b-2 border-green-300">
              <h3 class="font-semibold text-green-700">Completed</h3>
              <div class="flex items-center gap-2">
                <button
                  @click="showQuickAdd.completed = !showQuickAdd.completed"
                  class="text-green-400 hover:text-green-600 transition"
                  title="Quick add task"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                </button>
                <span class="text-sm text-gray-500">{{ getTasksByStatus('completed').length }}</span>
              </div>
            </div>

            <!-- Quick Add Form -->
            <div v-if="showQuickAdd.completed" class="mb-2">
              <input
                v-model="quickTaskTitle.completed"
                @keyup.enter="createQuickTask('completed')"
                @keyup.esc="showQuickAdd.completed = false"
                type="text"
                placeholder="Task title... (Enter to save)"
                class="w-full px-3 py-2 text-sm border border-green-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                autofocus
              />
            </div>

            <div
              class="space-y-2 flex-1 min-h-[200px]"
              @dragover.prevent
              @drop="handleDrop($event, 'completed')"
            >
              <div
                v-for="task in getTasksByStatus('completed')"
                :key="task.id"
                draggable="true"
                @dragstart="handleDragStart($event, task)"
                @click="openTaskDetail(task.id)"
                class="bg-green-50 p-3 rounded border border-green-200 hover:border-green-400 hover:shadow-md cursor-move transition group"
              >
                <div class="flex items-start justify-between mb-1">
                  <h5 class="font-medium text-gray-900 text-sm flex-1">{{ task.title }}</h5>
                  <button
                    @click.stop="editTaskInline(task)"
                    class="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-green-600 transition ml-2"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                  </button>
                </div>
                <p v-if="task.description" class="text-xs text-gray-600 line-clamp-2 mb-2">{{ task.description }}</p>
                <div v-if="task.due_date" class="flex items-center text-xs mt-1" :class="getDueDateClass(task.due_date)">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  {{ formatDueDate(task.due_date) }}
                </div>
                <div class="flex items-center justify-between mt-2">
                  <select
                    v-model="task.priority"
                    @click.stop
                    @change="updateTaskPriority(task)"
                    class="px-2 py-1 text-xs font-medium rounded border-0 cursor-pointer"
                    :class="getPriorityClass(task.priority)"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                  <span v-if="task.assignee_name" class="text-xs text-gray-500">
                    {{ task.assignee_name.split(' ')[0] }}
                  </span>
                </div>
              </div>
              <div v-if="getTasksByStatus('completed').length === 0 && !showQuickAdd.completed" class="text-center py-8 text-sm text-gray-400">
                No tasks
              </div>
            </div>
          </div>

          <!-- Blocked Column -->
          <div class="flex flex-col">
            <div class="flex items-center justify-between mb-3 pb-2 border-b-2 border-red-300">
              <h3 class="font-semibold text-red-700">Blocked</h3>
              <div class="flex items-center gap-2">
                <button
                  @click="showQuickAdd.blocked = !showQuickAdd.blocked"
                  class="text-red-400 hover:text-red-600 transition"
                  title="Quick add task"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                </button>
                <span class="text-sm text-gray-500">{{ getTasksByStatus('blocked').length }}</span>
              </div>
            </div>

            <!-- Quick Add Form -->
            <div v-if="showQuickAdd.blocked" class="mb-2">
              <input
                v-model="quickTaskTitle.blocked"
                @keyup.enter="createQuickTask('blocked')"
                @keyup.esc="showQuickAdd.blocked = false"
                type="text"
                placeholder="Task title... (Enter to save)"
                class="w-full px-3 py-2 text-sm border border-red-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
                autofocus
              />
            </div>

            <div
              class="space-y-2 flex-1 min-h-[200px]"
              @dragover.prevent
              @drop="handleDrop($event, 'blocked')"
            >
              <div
                v-for="task in getTasksByStatus('blocked')"
                :key="task.id"
                draggable="true"
                @dragstart="handleDragStart($event, task)"
                @click="openTaskDetail(task.id)"
                class="bg-red-50 p-3 rounded border border-red-200 hover:border-red-400 hover:shadow-md cursor-move transition group"
              >
                <div class="flex items-start justify-between mb-1">
                  <h5 class="font-medium text-gray-900 text-sm flex-1">{{ task.title }}</h5>
                  <button
                    @click.stop="editTaskInline(task)"
                    class="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-600 transition ml-2"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                  </button>
                </div>
                <p v-if="task.description" class="text-xs text-gray-600 line-clamp-2 mb-2">{{ task.description }}</p>
                <div v-if="task.due_date" class="flex items-center text-xs mt-1" :class="getDueDateClass(task.due_date)">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  {{ formatDueDate(task.due_date) }}
                </div>
                <div class="flex items-center justify-between mt-2">
                  <select
                    v-model="task.priority"
                    @click.stop
                    @change="updateTaskPriority(task)"
                    class="px-2 py-1 text-xs font-medium rounded border-0 cursor-pointer"
                    :class="getPriorityClass(task.priority)"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                  <span v-if="task.assignee_name" class="text-xs text-gray-500">
                    {{ task.assignee_name.split(' ')[0] }}
                  </span>
                </div>
              </div>
              <div v-if="getTasksByStatus('blocked').length === 0 && !showQuickAdd.blocked" class="text-center py-8 text-sm text-gray-400">
                No tasks
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- List View -->
      <div v-if="currentView === 'list'" class="bg-white shadow rounded-lg">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Task</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Assignee</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="task in allTasks"
                :key="task.id"
                class="hover:bg-gray-50 cursor-pointer transition"
                @click="openTaskDetail(task.id)"
              >
                <td class="px-6 py-4">
                  <div class="text-sm font-medium text-gray-900">{{ task.title }}</div>
                  <div v-if="task.description" class="text-sm text-gray-500 line-clamp-1">{{ task.description }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <select
                    v-model="task.status"
                    @click.stop
                    @change="updateTaskStatus(task)"
                    class="text-xs font-medium rounded-full px-3 py-1 border-0 cursor-pointer"
                    :class="getStatusClass(task.status)"
                  >
                    <option value="todo">To Do</option>
                    <option value="in_progress">In Progress</option>
                    <option value="in_review">In Review</option>
                    <option value="completed">Completed</option>
                    <option value="blocked">Blocked</option>
                  </select>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <select
                    v-model="task.priority"
                    @click.stop
                    @change="updateTaskPriority(task)"
                    class="text-xs font-medium rounded px-2 py-1 border-0 cursor-pointer"
                    :class="getPriorityClass(task.priority)"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ task.assignee_name || 'Unassigned' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span v-if="task.due_date" class="text-xs" :class="getDueDateClass(task.due_date)">
                    {{ formatDueDate(task.due_date) }}
                  </span>
                  <span v-else class="text-xs text-gray-400">No deadline</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button
                    @click.stop="editTaskInline(task)"
                    class="text-primary-600 hover:text-primary-900"
                  >
                    Edit
                  </button>
                </td>
              </tr>
              <tr v-if="allTasks.length === 0">
                <td colspan="6" class="px-6 py-8 text-center text-gray-500">
                  No tasks yet. Create your first task!
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Calendar View -->
      <div v-if="currentView === 'calendar'" class="bg-white shadow rounded-lg p-6">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Tasks by Due Date</h3>
        </div>

        <div class="space-y-4">
          <!-- Overdue Tasks -->
          <div v-if="overdueTasks.length > 0" class="border-l-4 border-red-500 pl-4">
            <h4 class="text-sm font-semibold text-red-700 mb-2 flex items-center">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Overdue ({{ overdueTasks.length }})
            </h4>
            <div class="space-y-2">
              <div
                v-for="task in overdueTasks"
                :key="task.id"
                @click="openTaskDetail(task.id)"
                class="bg-red-50 border border-red-200 rounded-lg p-3 cursor-pointer hover:shadow-md transition"
              >
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <h5 class="font-medium text-gray-900 text-sm">{{ task.title }}</h5>
                    <div class="flex items-center gap-2 mt-1">
                      <span class="text-xs px-2 py-0.5 rounded" :class="getStatusClass(task.status)">
                        {{ formatStatus(task.status) }}
                      </span>
                      <span class="text-xs text-red-600 font-medium">{{ formatDueDate(task.due_date) }}</span>
                    </div>
                  </div>
                  <span v-if="task.assignee_name" class="text-xs text-gray-600">{{ task.assignee_name.split(' ')[0] }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Due Today -->
          <div v-if="todayTasks.length > 0" class="border-l-4 border-orange-500 pl-4">
            <h4 class="text-sm font-semibold text-orange-700 mb-2">Due Today ({{ todayTasks.length }})</h4>
            <div class="space-y-2">
              <div
                v-for="task in todayTasks"
                :key="task.id"
                @click="openTaskDetail(task.id)"
                class="bg-orange-50 border border-orange-200 rounded-lg p-3 cursor-pointer hover:shadow-md transition"
              >
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <h5 class="font-medium text-gray-900 text-sm">{{ task.title }}</h5>
                    <div class="flex items-center gap-2 mt-1">
                      <span class="text-xs px-2 py-0.5 rounded" :class="getStatusClass(task.status)">
                        {{ formatStatus(task.status) }}
                      </span>
                    </div>
                  </div>
                  <span v-if="task.assignee_name" class="text-xs text-gray-600">{{ task.assignee_name.split(' ')[0] }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Due This Week -->
          <div v-if="thisWeekTasks.length > 0" class="border-l-4 border-yellow-500 pl-4">
            <h4 class="text-sm font-semibold text-yellow-700 mb-2">Due This Week ({{ thisWeekTasks.length }})</h4>
            <div class="space-y-2">
              <div
                v-for="task in thisWeekTasks"
                :key="task.id"
                @click="openTaskDetail(task.id)"
                class="bg-yellow-50 border border-yellow-200 rounded-lg p-3 cursor-pointer hover:shadow-md transition"
              >
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <h5 class="font-medium text-gray-900 text-sm">{{ task.title }}</h5>
                    <div class="flex items-center gap-2 mt-1">
                      <span class="text-xs px-2 py-0.5 rounded" :class="getStatusClass(task.status)">
                        {{ formatStatus(task.status) }}
                      </span>
                      <span class="text-xs text-gray-600">{{ formatDueDate(task.due_date) }}</span>
                    </div>
                  </div>
                  <span v-if="task.assignee_name" class="text-xs text-gray-600">{{ task.assignee_name.split(' ')[0] }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Later -->
          <div v-if="laterTasks.length > 0" class="border-l-4 border-gray-300 pl-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-2">Later ({{ laterTasks.length }})</h4>
            <div class="space-y-2">
              <div
                v-for="task in laterTasks"
                :key="task.id"
                @click="openTaskDetail(task.id)"
                class="bg-gray-50 border border-gray-200 rounded-lg p-3 cursor-pointer hover:shadow-md transition"
              >
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <h5 class="font-medium text-gray-900 text-sm">{{ task.title }}</h5>
                    <div class="flex items-center gap-2 mt-1">
                      <span class="text-xs px-2 py-0.5 rounded" :class="getStatusClass(task.status)">
                        {{ formatStatus(task.status) }}
                      </span>
                      <span class="text-xs text-gray-600">{{ formatDueDate(task.due_date) }}</span>
                    </div>
                  </div>
                  <span v-if="task.assignee_name" class="text-xs text-gray-600">{{ task.assignee_name.split(' ')[0] }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- No Due Date -->
          <div v-if="noDueDateTasks.length > 0" class="border-l-4 border-gray-200 pl-4">
            <h4 class="text-sm font-semibold text-gray-500 mb-2">No Due Date ({{ noDueDateTasks.length }})</h4>
            <div class="space-y-2">
              <div
                v-for="task in noDueDateTasks"
                :key="task.id"
                @click="openTaskDetail(task.id)"
                class="bg-white border border-gray-200 rounded-lg p-3 cursor-pointer hover:shadow-md transition"
              >
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <h5 class="font-medium text-gray-900 text-sm">{{ task.title }}</h5>
                    <div class="flex items-center gap-2 mt-1">
                      <span class="text-xs px-2 py-0.5 rounded" :class="getStatusClass(task.status)">
                        {{ formatStatus(task.status) }}
                      </span>
                    </div>
                  </div>
                  <span v-if="task.assignee_name" class="text-xs text-gray-600">{{ task.assignee_name.split(' ')[0] }}</span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="allTasks.length === 0" class="text-center py-12 text-gray-500">
            No tasks yet. Create your first task!
          </div>
        </div>
      </div>
    </div>

    <!-- Create Task Modal -->
    <div v-if="showCreateTask" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="showCreateTask = false">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white" @click.stop>
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Create Task</h3>
          <form @submit.prevent="handleCreateTask" class="space-y-4">
            <div>
              <label for="taskTitle" class="block text-sm font-medium text-gray-700">Task Title</label>
              <input
                id="taskTitle"
                v-model="taskForm.title"
                type="text"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Enter task title"
              />
            </div>
            <div>
              <label for="taskDescription" class="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                id="taskDescription"
                v-model="taskForm.description"
                rows="3"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Enter task description"
              />
            </div>
            <div>
              <label for="priority" class="block text-sm font-medium text-gray-700">Priority</label>
              <select
                id="priority"
                v-model="taskForm.priority"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
            <div>
              <label for="assignee" class="block text-sm font-medium text-gray-700">Assign To</label>
              <select
                id="assignee"
                v-model="taskForm.assignee_id"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                <option :value="null">Unassigned</option>
                <option v-for="member in workspaceMembers" :key="member.user_id" :value="member.user_id">
                  {{ member.full_name || member.username }}
                </option>
              </select>
            </div>
            <div class="flex justify-end space-x-3 mt-5">
              <button
                type="button"
                @click="showCreateTask = false"
                class="px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-md border border-gray-300 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="creatingTask"
                class="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-md hover:bg-primary-700 disabled:opacity-50"
              >
                {{ creatingTask ? 'Creating...' : 'Create' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useWorkspaceStore } from '@/stores/workspace'
import { useTaskStore } from '@/stores/task'
import { useAuthStore } from '@/stores/auth'
import { TaskStatus, TaskPriority, type Task } from '@/types/task'
import { workspaceService } from '@/services/workspace.service'
import { format, isToday, isThisWeek, isPast, parseISO, differenceInDays } from 'date-fns'

const route = useRoute()
const router = useRouter()
const workspaceStore = useWorkspaceStore()
const taskStore = useTaskStore()
const authStore = useAuthStore()

// View state
const currentView = ref<'board' | 'list' | 'calendar'>('board')

const showCreateTask = ref(false)
const creatingTask = ref(false)
const workspaceMembers = ref<any[]>([])
const projectId = ref(0)
const taskForm = ref({
  title: '',
  description: '',
  project_id: 0,
  assignee_id: null as number | null,
  priority: TaskPriority.MEDIUM,
  status: TaskStatus.TODO
})

// Computed properties for different views
const allTasks = computed(() => {
  return workspaceStore.currentProject?.tasks || []
})

const overdueTasks = computed(() => {
  return allTasks.value.filter(task => {
    if (!task.due_date || task.status === 'completed') return false
    return isPast(parseISO(task.due_date)) && !isToday(parseISO(task.due_date))
  })
})

const todayTasks = computed(() => {
  return allTasks.value.filter(task => {
    if (!task.due_date || task.status === 'completed') return false
    return isToday(parseISO(task.due_date))
  })
})

const thisWeekTasks = computed(() => {
  return allTasks.value.filter(task => {
    if (!task.due_date || task.status === 'completed') return false
    const dueDate = parseISO(task.due_date)
    return isThisWeek(dueDate) && !isToday(dueDate) && !isPast(dueDate)
  })
})

const laterTasks = computed(() => {
  return allTasks.value.filter(task => {
    if (!task.due_date || task.status === 'completed') return false
    const dueDate = parseISO(task.due_date)
    return !isThisWeek(dueDate) && !isPast(dueDate)
  })
})

const noDueDateTasks = computed(() => {
  return allTasks.value.filter(task => !task.due_date && task.status !== 'completed')
})

// Quick add task functionality
const showQuickAdd = ref({
  todo: false,
  in_progress: false,
  in_review: false,
  completed: false,
  blocked: false
})

const quickTaskTitle = ref({
  todo: '',
  in_progress: '',
  in_review: '',
  completed: '',
  blocked: ''
})

// Drag and drop state
const draggedTask = ref<Task | null>(null)

// Load project data helper function
const loadProjectData = async (id: number) => {
  projectId.value = id
  taskForm.value.project_id = id
  await workspaceStore.fetchProject(id)

  // Fetch workspace members for assignee dropdown
  if (workspaceStore.currentProject?.workspace_id) {
    try {
      workspaceMembers.value = await workspaceService.getWorkspaceMembers(workspaceStore.currentProject.workspace_id)
    } catch (error) {
      console.error('Failed to fetch workspace members:', error)
    }
  }
}

onMounted(async () => {
  const id = parseInt(route.params.id as string)
  await loadProjectData(id)
})

// Watch for route parameter changes to reload project data when switching between projects
watch(() => route.params.id, async (newId) => {
  if (newId && route.name === 'project') {
    const id = parseInt(newId as string)
    await loadProjectData(id)
  }
})

const getTasksByStatus = (status: string): Task[] => {
  if (!workspaceStore.currentProject?.tasks) return []
  return workspaceStore.currentProject.tasks.filter(task => task.status === status)
}

const getPriorityClass = (priority: string) => {
  const classes = {
    'low': 'bg-yellow-100 text-yellow-800',
    'medium': 'bg-blue-100 text-blue-800',
    'high': 'bg-orange-100 text-orange-800',
    'urgent': 'bg-red-100 text-red-800'
  }
  return classes[priority as keyof typeof classes] || classes.medium
}

// Date formatting and utilities
const formatDueDate = (date: string | undefined) => {
  if (!date) return ''
  const dueDate = parseISO(date)
  const today = new Date()
  const diffDays = differenceInDays(dueDate, today)

  if (isToday(dueDate)) return 'Today'
  if (diffDays === 1) return 'Tomorrow'
  if (diffDays === -1) return 'Yesterday'
  if (diffDays < -1) return format(dueDate, 'MMM d') + ' (overdue)'
  if (diffDays <= 7) return format(dueDate, 'EEE, MMM d')
  return format(dueDate, 'MMM d, yyyy')
}

const getDueDateClass = (date: string | undefined) => {
  if (!date) return ''
  const dueDate = parseISO(date)

  if (isPast(dueDate) && !isToday(dueDate)) return 'text-red-600 font-semibold'
  if (isToday(dueDate)) return 'text-orange-600 font-semibold'
  if (isThisWeek(dueDate)) return 'text-yellow-600'
  return 'text-gray-600'
}

const getStatusClass = (status: string) => {
  const classes = {
    'todo': 'bg-gray-100 text-gray-800',
    'in_progress': 'bg-blue-100 text-blue-800',
    'in_review': 'bg-purple-100 text-purple-800',
    'completed': 'bg-green-100 text-green-800',
    'blocked': 'bg-red-100 text-red-800'
  }
  return classes[status as keyof typeof classes] || classes.todo
}

const formatStatus = (status: string) => {
  return status.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

const updateTaskStatus = async (task: Task) => {
  try {
    await taskStore.updateTask(task.id, { status: task.status as TaskStatus })
    await workspaceStore.fetchProject(projectId.value)
  } catch (error) {
    console.error('Failed to update task status:', error)
  }
}

// Quick task creation
const createQuickTask = async (status: string) => {
  const title = quickTaskTitle.value[status as keyof typeof quickTaskTitle.value]
  if (!title.trim()) return

  try {
    await taskStore.createTask({
      title: title.trim(),
      project_id: projectId.value,
      status: status as TaskStatus,
      priority: TaskPriority.MEDIUM,
      assignee_id: authStore.user?.id
    })

    // Clear input and hide form
    quickTaskTitle.value[status as keyof typeof quickTaskTitle.value] = ''
    showQuickAdd.value[status as keyof typeof showQuickAdd.value] = false

    // Refresh project
    await workspaceStore.fetchProject(projectId.value)
  } catch (error) {
    console.error('Failed to create task:', error)
  }
}

// Drag and drop handlers
const handleDragStart = (event: DragEvent, task: Task) => {
  draggedTask.value = task
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move'
  }
}

const handleDrop = async (event: DragEvent, newStatus: string) => {
  event.preventDefault()

  if (!draggedTask.value || draggedTask.value.status === newStatus) {
    draggedTask.value = null
    return
  }

  try {
    await taskStore.updateTask(draggedTask.value.id, { status: newStatus as TaskStatus })
    await workspaceStore.fetchProject(projectId.value)
  } catch (error) {
    console.error('Failed to update task status:', error)
  } finally {
    draggedTask.value = null
  }
}

// Inline priority update
const updateTaskPriority = async (task: Task) => {
  try {
    await taskStore.updateTask(task.id, { priority: task.priority })
  } catch (error) {
    console.error('Failed to update task priority:', error)
    // Refresh to revert on error
    await workspaceStore.fetchProject(projectId.value)
  }
}

// Navigate to task detail
const openTaskDetail = (taskId: number) => {
  router.push({ name: 'task', params: { id: taskId } })
}

// Inline editing (opens detail page for now, can be enhanced later)
const editTaskInline = (task: Task) => {
  router.push({ name: 'task', params: { id: task.id } })
}

const openCreateTask = () => {
  // Set current user as default assignee
  taskForm.value.assignee_id = authStore.user?.id ?? null
  showCreateTask.value = true
}

const handleCreateTask = async () => {
  try {
    creatingTask.value = true
    // Convert null to undefined for API compatibility
    const taskData = {
      ...taskForm.value,
      assignee_id: taskForm.value.assignee_id ?? undefined
    }
    await taskStore.createTask(taskData)
    showCreateTask.value = false
    taskForm.value.title = ''
    taskForm.value.description = ''
    taskForm.value.assignee_id = null
    taskForm.value.priority = TaskPriority.MEDIUM
    taskForm.value.status = TaskStatus.TODO
    // Refresh project to show new task
    await workspaceStore.fetchProject(projectId.value)
  } catch (error) {
    console.error('Failed to create task:', error)
  } finally {
    creatingTask.value = false
  }
}
</script>
