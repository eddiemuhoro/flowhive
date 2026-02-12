# Field Settings Components

This directory contains modular components for the Field Operations Settings page.

## Structure

```
settings/
├── index.ts                          # Central exports
├── TaskCategoriesSection.vue         # Task category management
├── TeamMembersSection.vue            # Team member management
├── PermissionSettingsSection.vue     # Permission documentation
└── WorkspaceSettingsSection.vue      # Workspace configuration
```

## Components

### TaskCategoriesSection.vue
**Purpose**: Manages task categories for field activities

**Props**:
- `workspaceId: number` - Current workspace ID

**Features**:
- Create/edit/deactivate categories
- Color and icon customization
- Auto-slug generation
- Active/inactive state management

**State**: Self-contained with category store integration

---

### TeamMembersSection.vue
**Purpose**: Manages workspace team members

**Props**:
- `workspace: WorkspaceDetail | null` - Current workspace data
- `currentUserId: number | undefined` - Logged-in user ID
- `currentUserRole: string | undefined` - User's system role

**Features**:
- Add/remove members
- Change member workspace roles (member/manager)
- User search functionality
- Role-based access control

**State**: Self-contained with workspace store integration

---

### PermissionSettingsSection.vue
**Purpose**: Displays permission documentation

**Props**: None (presentational component)

**Features**:
- Shows what each role can do
- Three-tier permission structure:
  - Member (default)
  - Manager (elevated)
  - Executive & Owner (full access)

**State**: No state - pure UI component

---

### WorkspaceSettingsSection.vue
**Purpose**: Manages workspace-level settings

**Props**:
- `workspace: WorkspaceDetail | null` - Current workspace data
- `currentUserId: number | undefined` - Logged-in user ID
- `currentUserRole: string | undefined` - User's system role

**Features**:
- Edit workspace name
- Delete workspace (with confirmation)
- Role-based access control

**State**: Self-contained with workspace store integration

---

## Usage

Import components individually:
```typescript
import TaskCategoriesSection from './components/settings/TaskCategoriesSection.vue';
```

Or use the index file:
```typescript
import { TaskCategoriesSection, TeamMembersSection } from './components/settings';
```

## Design Principles

1. **Single Responsibility**: Each component handles one distinct section
2. **Self-Contained**: Components manage their own state and logic
3. **Prop-Based Communication**: Parent passes minimal props, components handle the rest
4. **Store Integration**: Components directly interact with stores (no prop drilling)
5. **Consistent Styling**: All sections use the same card-based layout

## Benefits

- **Maintainability**: Easy to locate and update specific features
- **Testability**: Each component can be tested independently
- **Reusability**: Components can be reused in other views if needed
- **Performance**: Smaller components are easier to optimize
- **Readability**: Clear separation of concerns
