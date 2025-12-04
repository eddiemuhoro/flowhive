import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '@/services/auth.service'
import type { User, LoginRequest, RegisterRequest } from '@/types/auth'
import { UserRole } from '@/types/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isExecutive = computed(() => user.value?.role === 'executive')
  const isManager = computed(() => user.value?.role === 'manager' || isExecutive.value)

  async function login(credentials: LoginRequest) {
    try {
      loading.value = true
      error.value = null

      // Mock login for development without backend
      token.value = 'mock-token-' + Date.now()
      localStorage.setItem('access_token', token.value)

      // Mock user data
      user.value = {
        id: 1,
        email: credentials.username,
        username: credentials.username,
        full_name: 'Mock User',
        role: UserRole.EXECUTIVE,
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }

      // Uncomment when backend is ready:
      // const response = await authService.login(credentials)
      // token.value = response.access_token
      // localStorage.setItem('access_token', response.access_token)
      // await fetchCurrentUser()
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function register(data: RegisterRequest) {
    try {
      loading.value = true
      error.value = null

      await authService.register(data)

      // Auto login after registration
      await login({
        username: data.username,
        password: data.password
      })
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Registration failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchCurrentUser() {
    try {
      // Mock: Skip fetching if user already exists (mock mode)
      if (user.value) return

      // Uncomment when backend is ready:
      // user.value = await authService.getCurrentUser()
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch user'
      logout()
      throw err
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('access_token')
  }

  async function initialize() {
    if (token.value) {
      try {
        await fetchCurrentUser()
      } catch {
        logout()
      }
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    isExecutive,
    isManager,
    login,
    register,
    logout,
    fetchCurrentUser,
    initialize
  }
})
