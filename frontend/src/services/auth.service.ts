import { apiClient } from './api'
import type { User, LoginRequest, RegisterRequest, AuthResponse } from '@/types/auth'

export const authService = {
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    const response = await apiClient.post<AuthResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  async register(data: RegisterRequest): Promise<User> {
    const response = await apiClient.post<User>('/auth/register', data)
    return response.data
  },

  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<User>('/auth/me')
    return response.data
  },

  async forgotPassword(email: string): Promise<{ message: string; reset_token: string | null }> {
    const response = await apiClient.post<{ message: string; reset_token: string | null }>('/auth/forgot-password', { email })
    return response.data
  },

  async resetPassword(token: string, new_password: string): Promise<{ message: string }> {
    const response = await apiClient.post<{ message: string }>('/auth/reset-password', {
      token,
      new_password
    })
    return response.data
  }
}
