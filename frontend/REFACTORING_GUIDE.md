# ProjectDetail Component Refactoring Guide

## Overview
This guide explains how to refactor the large `ProjectDetail.vue` component (~1200 lines) into smaller, maintainable pieces following Vue 3 composition API best practices.

## Current Problems
- ❌ Single file with 1200+ lines
- ❌ Mixed concerns (UI, business logic, data fetching)
- ❌ Difficult to test individual features
- ❌ Hard for multiple developers to work on simultaneously
- ❌ Repeated code across board columns

## Proposed Structure

```
src/
├── components/
│   ├── project/
│   │   ├── ProjectHeader.vue          # ~50 lines
│   │   ├── CreateTaskModal.vue        # ~150 lines
│   │   ├── board/
│   │   │   ├── BoardView.vue          # ~100 lines
│   │   │   ├── BoardColumn.vue        # ~150 lines (reusable for all 5 columns)
│   │   │   ├── TaskCard.vue           # ~80 lines ✅ CREATED
│   │   │   └── QuickAddForm.vue       # ~70 lines ✅ CREATED
│   │   ├── list/
│   │   │   ├── ListView.vue           # ~120 lines
│   │   │   └── TaskRow.vue            # ~60 lines
│   │   └── calendar/
│   │       ├── CalendarView.vue       # ~150 lines
│   │       └── TaskGroup.vue          # ~80 lines
│   └── ui/
│       └── ViewSwitcher.vue           # ~40 lines ✅ CREATED
├── composables/                       # ✅ ALL CREATED
│   ├── useTaskFormatting.ts           # Date/status formatting
│   ├── useTaskFilters.ts              # Filter tasks by status/date
│   └── useTaskDragDrop.ts             # Drag & drop logic
└── views/
    └── ProjectDetail.vue              # ~150 lines (orchestrator)
```

## Created Files ✅

### 1. Composables (Business Logic)
- ✅ `useTaskFormatting.ts` - All formatting utilities
- ✅ `useTaskFilters.ts` - Task filtering by status and date
- ✅ `useTaskDragDrop.ts` - Drag and drop functionality

### 2. Reusable Components
- ✅ `TaskCard.vue` - Single task card (works for all statuses)
- ✅ `QuickAddForm.vue` - Quick add form (reusable for all columns)
- ✅ `ViewSwitcher.vue` - View toggle buttons

## Next Steps

### Step 1: Create BoardColumn Component
Create a reusable column component that replaces the 5 duplicate column blocks:

```vue
<!-- src/components/project/board/BoardColumn.vue -->
<template>
  <div class="flex flex-col">
    <div class="flex items-center justify-between mb-3 pb-2 border-b-2" :class="headerBorderClass">
      <h3 class="font-semibold" :class="headerTextClass">{{ title }}</h3>
      <div class="flex items-center gap-2">
        <button @click="toggleQuickAdd" :class="addButtonClass">
          <!-- + icon -->
        </button>
        <span class="text-sm text-gray-500">{{ tasks.length }}</span>
      </div>
    </div>

    <QuickAddForm
      :show="showQuickAdd"
      :status="status"
      :inputClasses="formInputClasses"
      :buttonClasses="formButtonClasses"
      @submit="handleQuickAdd"
      @cancel="showQuickAdd = false"
    />

    <div @dragover.prevent @drop="handleDrop" class="space-y-2 flex-1 min-h-[200px]">
      <TaskCard
        v-for="task in tasks"
        :key="task.id"
        :task="task"
        :cardClasses="taskCardClasses"
        @dragstart="handleDragStart"
        @click="handleTaskClick"
        @edit="handleEdit"
        @updatePriority="handlePriorityUpdate"
      />
    </div>
  </div>
</template>
```

### Step 2: Create BoardView Component
Wrap all columns in a container:

```vue
<!-- src/components/project/board/BoardView.vue -->
<template>
  <div class="bg-white shadow rounded-lg p-6">
    <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
      <BoardColumn
        v-for="column in columns"
        :key="column.status"
        :status="column.status"
        :title="column.title"
        :tasks="getTasksByStatus(column.status)"
        :headerBorderClass="column.borderClass"
        :headerTextClass="column.textClass"
        :addButtonClass="column.buttonClass"
        :formInputClasses="column.inputClass"
        :formButtonClasses="column.buttonBgClass"
        :taskCardClasses="column.cardClass"
        @quickAdd="handleQuickAdd"
        @dragDrop="handleDragDrop"
        @taskClick="handleTaskClick"
        @taskEdit="handleTaskEdit"
        @priorityUpdate="handlePriorityUpdate"
      />
    </div>
  </div>
</template>
```

### Step 3: Refactor Main ProjectDetail.vue

```vue
<!-- src/views/ProjectDetail.vue -->
<template>
  <div>
    <ProjectHeader
      :project="workspaceStore.currentProject"
      v-model:currentView="currentView"
      @createTask="showCreateTask = true"
    />

    <BoardView v-if="currentView === 'board'" :projectId="projectId" />
    <ListView v-else-if="currentView === 'list'" :projectId="projectId" />
    <CalendarView v-else-if="currentView === 'calendar'" :projectId="projectId" />

    <CreateTaskModal
      v-if="showCreateTask"
      :projectId="projectId"
      :workspaceMembers="workspaceMembers"
      @close="showCreateTask = false"
      @created="handleTaskCreated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useWorkspaceStore } from '@/stores/workspace'
import { workspaceService } from '@/services/workspace.service'
import ProjectHeader from '@/components/project/ProjectHeader.vue'
import BoardView from '@/components/project/board/BoardView.vue'
import ListView from '@/components/project/list/ListView.vue'
import CalendarView from '@/components/project/calendar/CalendarView.vue'
import CreateTaskModal from '@/components/project/CreateTaskModal.vue'

const route = useRoute()
const workspaceStore = useWorkspaceStore()
const currentView = ref<'board' | 'list' | 'calendar'>('board')
const showCreateTask = ref(false)
const workspaceMembers = ref<any[]>([])
const projectId = ref(0)

const loadProjectData = async (id: number) => {
  projectId.value = id
  await workspaceStore.fetchProject(id)

  if (workspaceStore.currentProject?.workspace_id) {
    try {
      workspaceMembers.value = await workspaceService.getWorkspaceMembers(
        workspaceStore.currentProject.workspace_id
      )
    } catch (error) {
      console.error('Failed to fetch workspace members:', error)
    }
  }
}

onMounted(async () => {
  const id = parseInt(route.params.id as string)
  await loadProjectData(id)
})

watch(() => route.params.id, async (newId) => {
  if (newId && route.name === 'project') {
    await loadProjectData(parseInt(newId as string))
  }
})

const handleTaskCreated = async () => {
  await workspaceStore.fetchProject(projectId.value)
}
</script>
```

## Benefits of This Approach

### Before (Current State)
- 1 file: 1,200 lines
- All logic mixed together
- Hard to test
- Duplicate code (5 board columns)
- Difficult for teams to collaborate

### After (Refactored)
- 15+ focused files: 50-150 lines each
- Clear separation of concerns
- Easy to test individual pieces
- Reusable components (1 BoardColumn = 5 instances)
- Multiple devs can work simultaneously

## Testing Strategy

### Unit Tests
```typescript
// composables/useTaskFormatting.spec.ts
describe('useTaskFormatting', () => {
  it('formats due date as "Today"', () => {
    const { formatDueDate } = useTaskFormatting()
    expect(formatDueDate(todayDate)).toBe('Today')
  })
})

// components/TaskCard.spec.ts
describe('TaskCard', () => {
  it('emits click event when clicked', async () => {
    const wrapper = mount(TaskCard, { props: { task: mockTask } })
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })
})
```

### Component Tests
```typescript
// components/board/BoardColumn.spec.ts
describe('BoardColumn', () => {
  it('renders correct number of tasks', () => {
    const wrapper = mount(BoardColumn, {
      props: { tasks: [task1, task2], status: 'todo' }
    })
    expect(wrapper.findAllComponents(TaskCard)).toHaveLength(2)
  })
})
```

## Migration Strategy

### Phase 1: Create Infrastructure ✅
- ✅ Create folder structure
- ✅ Create composables
- ✅ Create basic reusable components

### Phase 2: Extract Components (Recommended Order)
1. Extract `TaskCard.vue` ✅
2. Extract `QuickAddForm.vue` ✅
3. Extract `BoardColumn.vue` (this eliminates 80% of duplication)
4. Extract `BoardView.vue`
5. Extract `ProjectHeader.vue`
6. Extract `CreateTaskModal.vue`
7. Extract `ListView.vue` and `TaskRow.vue`
8. Extract `CalendarView.vue` and `TaskGroup.vue`

### Phase 3: Refactor Main View
- Update `ProjectDetail.vue` to use new components
- Remove old code as components are integrated
- Test each integration step

### Phase 4: Testing & Polish
- Add unit tests for composables
- Add component tests
- Add e2e tests for critical paths
- Performance optimization

## Performance Considerations

### Before
- Entire 1200-line component re-renders on any change
- All 5 columns re-render even if only 1 changes
- Heavy computation in template

### After
- Only affected components re-render
- BoardColumn instances are independent
- Composables are optimized with computed refs
- Better tree-shaking (smaller bundle)

## Conclusion

This refactoring will:
- ✅ Reduce main file from 1200 → 150 lines (88% reduction)
- ✅ Create 15+ focused, testable components
- ✅ Enable parallel development by teams
- ✅ Improve performance through better reactivity
- ✅ Make codebase more maintainable long-term
- ✅ Follow Vue 3 composition API best practices

**Estimated Time:** 2-3 days for complete refactoring
**ROI:** Massive - saves weeks of future maintenance time
