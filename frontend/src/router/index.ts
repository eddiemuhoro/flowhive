import {
  createRouter,
  createWebHistory,
  type RouteLocationNormalized,
  type NavigationGuardNext,
} from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useWorkspaceStore } from "@/stores/workspace";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "login",
      component: () => import("@/views/Login.vue"),
      meta: { requiresAuth: false },
    },
    {
      path: "/register",
      name: "register",
      component: () => import("@/views/Register.vue"),
      meta: { requiresAuth: false },
    },
    // Field Operations Routes
    {
      path: "/field",
      component: () => import("@/layouts/FieldLayout.vue"),
      meta: { requiresAuth: true, workspaceType: "FIELD_OPERATIONS" },
      children: [
        {
          path: "",
          name: "field-dashboard",
          component: () => import("@/views/field/FieldDashboard.vue"),
        },
        {
          path: "activities",
          name: "field-activities",
          component: () => import("@/views/field/FieldActivityLog.vue"),
        },
        {
          path: "activities/:id",
          name: "field-activity-detail",
          component: () => import("@/views/field/FieldActivityDetail.vue"),
        },
        {
          path: "analytics",
          name: "field-analytics",
          component: () => import("@/views/field/FieldAnalytics.vue"),
          meta: { roles: ["manager", "executive"] },
        },
        {
          path: "settings",
          name: "field-settings",
          component: () => import("@/views/field/FieldSettings.vue"),
          meta: { roles: ["manager", "executive"] },
        },
      ],
    },
    // Project Management Routes
    {
      path: "/",
      component: () => import("@/layouts/MainLayout.vue"),
      meta: { requiresAuth: true, workspaceType: "PROJECT_MANAGEMENT" },
      children: [
        {
          path: "",
          name: "dashboard",
          component: () => import("@/views/Dashboard.vue"),
        },
        {
          path: "workspaces",
          name: "workspaces",
          component: () => import("@/views/Workspaces.vue"),
        },
        {
          path: "workspace/:id",
          name: "workspace",
          component: () => import("@/views/WorkspaceDetail.vue"),
        },
        {
          path: "project/:id",
          name: "project",
          component: () => import("@/views/ProjectDetail.vue"),
        },
        {
          path: "task/:id",
          name: "task",
          component: () => import("@/views/TaskDetail.vue"),
        },
        {
          path: "my-tasks",
          name: "my-tasks",
          component: () => import("@/views/MyTasks.vue"),
        },
        {
          path: "analytics",
          name: "analytics",
          component: () => import("@/views/Analytics.vue"),
          meta: { roles: ["manager", "executive"] },
        },
      ],
    },
  ],
});

// Track if auth has been initialized
let authInitialized = false;

router.beforeEach(
  async (
    to: RouteLocationNormalized,
    _from: RouteLocationNormalized,
    next: NavigationGuardNext,
  ) => {
    const authStore = useAuthStore();
    const workspaceStore = useWorkspaceStore();

    // Wait for auth initialization on first navigation
    if (!authInitialized) {
      await authStore.initialize();
      // Initialize workspace from localStorage after auth
      if (authStore.isAuthenticated) {
        await workspaceStore.initializeWorkspace();
      }
      authInitialized = true;
    }

    if (to.meta.requiresAuth !== false && !authStore.isAuthenticated) {
      next({ name: "login", query: { redirect: to.fullPath } });
    } else if (to.name === "login" && authStore.isAuthenticated) {
      // Redirect to appropriate dashboard based on current workspace type
      const currentWorkspace = workspaceStore.currentWorkspace;
      if (currentWorkspace?.workspace_type === "FIELD_OPERATIONS") {
        next("/field");
      } else {
        next({ name: "dashboard" });
      }
    } else if (
      to.meta.roles &&
      !to.meta.roles.includes(authStore.user?.role || "")
    ) {
      next({ name: "dashboard" });
    } else if (to.meta.workspaceType) {
      // Check workspace type for field operations routes
      const currentWorkspace = workspaceStore.currentWorkspace;
      if (
        currentWorkspace &&
        currentWorkspace.workspace_type !== to.meta.workspaceType
      ) {
        // Redirect to appropriate dashboard based on workspace type
        if (currentWorkspace.workspace_type === "FIELD_OPERATIONS") {
          next("/field");
        } else {
          next(`/workspace/${currentWorkspace.id}`);
        }
      } else {
        next();
      }
    } else {
      next();
    }
  },
);

export default router;
