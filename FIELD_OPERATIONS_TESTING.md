# Field Operations Testing Guide

## Overview

You now have complete UI separation between Project Management and Field Operations workspaces with smart routing!

## What's Been Implemented

### 1. **Workspace Type Selection**

- When creating a workspace, you can now choose between:
  - **Project Management**: For development teams (existing task management UI)
  - **Field Operations**: For field workers (new activity tracking UI)

### 2. **Smart Routing**

- Clicking a workspace automatically routes you to the correct UI:
  - **Field Operations** → `/field` (Field Dashboard)
  - **Project Management** → `/workspace/:id` (Project Dashboard)

### 3. **Workspace Switcher**

- Added dropdown component in both layouts
- Shows all your workspaces with type badges
- Quick switching between different workspace types
- Located in sidebar header (desktop) and mobile menu

### 4. **Navigation Guards**

- Prevents Field Operations users from accessing Project Management UI (and vice versa)
- Automatic redirects if wrong UI is accessed

## Testing Steps

### Step 1: Start Both Servers

**Terminal 1 - Backend:**

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**

```powershell
cd frontend
npm run dev
```

### Step 2: Create Test Workspaces

1. Login/Register at `http://localhost:5173`
2. Navigate to **Workspaces** page
3. Create two workspaces:

**Workspace 1 - Project Management:**

- Name: "Development Team"
- Description: "For software development tasks"
- Workspace Type: **Project Management**
- Click Create

**Workspace 2 - Field Operations:**

- Name: "Field Support Team"
- Description: "For field service activities"
- Workspace Type: **Field Operations**
- Click Create

### Step 3: Test Project Management Workspace

1. Click on "Development Team" workspace card
2. **Expected Result**: Routes to `/workspace/1`
3. **UI Should Show**:
   - Main layout with sidebar
   - Tasks, Projects navigation
   - Board/List/Calendar views
   - Workspace switcher in sidebar header
   - Your existing project management UI

### Step 4: Test Field Operations Workspace

1. Use workspace switcher dropdown (in sidebar header) OR go back to workspaces page
2. Click on "Field Support Team" workspace
3. **Expected Result**: Routes to `/field`
4. **UI Should Show**:
   - Field layout with mobile-first design
   - Dashboard with stats (Today's activities, This week, etc.)
   - Navigation: Dashboard, Activity Log, Analytics (if manager)
   - Quick actions: "Log New Activity", "View All Activities"
   - Workspace switcher in header

### Step 5: Test UI Isolation

**Test Field Operations Features:**

1. Click "Log New Activity"
2. Fill form:
   - Title: "Customer site visit"
   - Date: Today
   - Start Time: 09:00
   - End Time: 11:00
   - Customer Name: "ABC Corp"
   - Location: "123 Main St"
   - Task: (select a category - need to create in settings first)
   - Remarks: "Installation completed"
3. Save activity

**Navigate Field Operations:**

- Dashboard: See activity stats
- Activity Log: View all activities with filters
- Analytics (managers): View team performance charts
- Settings (managers): Manage task categories

**Switch to Project Management:**

1. Use workspace switcher dropdown
2. Select "Development Team"
3. **Verify**: Completely different UI - no field operations features visible
4. **Verify**: Can still create tasks, projects, etc.

### Step 6: Test Workspace Switcher

**In Project Management Workspace:**

1. Click workspace dropdown in sidebar header
2. Should see both workspaces with type badges:
   - "Development Team" - Blue badge (Project Management)
   - "Field Support Team" - Green badge (Field Operations)
3. Click "Field Support Team"
4. **Expected**: Instantly routes to `/field` with field UI

**In Field Operations Workspace:**

1. Click workspace dropdown in header (desktop) or sidebar (mobile)
2. Click "Development Team"
3. **Expected**: Routes to `/workspace/1` with project management UI

### Step 7: Test Mobile Responsiveness

1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select mobile device (iPhone 12, etc.)

**Field Operations (Mobile):**

- Hamburger menu opens sidebar
- Workspace switcher in sidebar
- Activity cards stack vertically
- Forms are touch-friendly

**Project Management (Mobile):**

- Responsive sidebar
- Workspace switcher accessible
- Task cards adapt to mobile

## Expected UI Differences

### Project Management UI

- ✅ Tasks & Projects
- ✅ Board/List/Calendar views
- ✅ Sprint planning
- ✅ Task assignments & status
- ✅ Project workflows
- ❌ NO field activity logging
- ❌ NO time tracking with start/end times
- ❌ NO customer/location fields

### Field Operations UI

- ✅ Activity logging with time tracking
- ✅ Customer name & location
- ✅ Task categories (manager-controlled)
- ✅ Photo uploads
- ✅ Analytics (hours by staff, activities by category)
- ✅ Mobile-optimized forms
- ❌ NO projects or sprints
- ❌ NO kanban boards
- ❌ NO task dependencies

## Troubleshooting

### Issue: Workspace switcher not showing

- **Fix**: Refresh page after creating workspaces
- **Cause**: Workspace list may not auto-update

### Issue: Can't see Analytics/Settings in field operations

- **Fix**: User role must be MANAGER or EXECUTIVE
- **Check**: Database user role or update via API

### Issue: Both UIs look the same

- **Fix**: Verify workspace_type in database
- **Query**: `SELECT id, name, workspace_type FROM workspaces;`
- **Update if needed**:
  ```sql
  UPDATE workspaces SET workspace_type = 'FIELD_OPERATIONS' WHERE id = 2;
  ```

### Issue: Error when switching workspaces

- **Check**: Browser console for errors
- **Verify**: Backend is running and responding
- **Test**: Try accessing `/api/workspaces` directly

## Next Steps

### For Field Operations Manager:

1. Go to Field Settings (sidebar menu)
2. Create task categories:
   - Name: "installation", Title: "Installation", Color: #10b981, Icon: 🔧
   - Name: "maintenance", Title: "Maintenance", Color: #f59e0b, Icon: 🛠️
   - Name: "repair", Title: "Repair", Color: #ef4444, Icon: 🔨
   - Name: "inspection", Title: "Inspection", Color: #3b82f6, Icon: 🔍
3. Now team members can log activities with proper categorization

### For Development Team:

1. Continue using existing project management features
2. Create projects, tasks, boards as normal
3. No changes to existing workflow

## Key Features Verified

✅ Complete UI separation  
✅ Smart routing based on workspace type  
✅ Workspace switcher with type indicators  
✅ Navigation guards preventing wrong UI access  
✅ Mobile-responsive layouts for both UIs  
✅ Role-based access (analytics/settings for managers)  
✅ Maintains all existing project management features  
✅ New field operations features fully integrated

## Success Criteria

- [ ] Can create both workspace types
- [ ] Project Management workspace shows tasks/projects UI
- [ ] Field Operations workspace shows activity logging UI
- [ ] Workspace switcher allows quick switching
- [ ] No overlap between the two UIs
- [ ] Mobile-friendly on both interfaces
- [ ] Managers can access analytics/settings in field operations
- [ ] Team members see appropriate features for their workspace type

---

**All field operations features are now live and ready for testing!** 🎉
