import { createRouter, createWebHistory, type RouteLocationNormalized, type NavigationGuardNext } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/Register.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: () => import('@/views/Dashboard.vue')
        },
        {
          path: 'workspaces',
          name: 'workspaces',
          component: () => import('@/views/Workspaces.vue')
        },
        {
          path: 'workspace/:id',
          name: 'workspace',
          component: () => import('@/views/WorkspaceDetail.vue')
        },
        {
          path: 'project/:id',
          name: 'project',
          component: () => import('@/views/ProjectDetail.vue')
        },
        {
          path: 'task/:id',
          name: 'task',
          component: () => import('@/views/TaskDetail.vue')
        },
        {
          path: 'my-tasks',
          name: 'my-tasks',
          component: () => import('@/views/MyTasks.vue')
        },
        {
          path: 'analytics',
          name: 'analytics',
          component: () => import('@/views/Analytics.vue'),
          meta: { roles: ['manager', 'executive'] }
        }
      ]
    }
  ]
})

router.beforeEach(async (to: RouteLocationNormalized, _from: RouteLocationNormalized, next: NavigationGuardNext) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth !== false && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.name === 'login' && authStore.isAuthenticated) {
    next({ name: 'dashboard' })
  } else if (to.meta.roles && !to.meta.roles.includes(authStore.user?.role || '')) {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
