import { apiClient } from './api'
import type { User } from '@/types/auth'

export interface UserUpdateData {
  email?: string
  username?: string
  full_name?: string
  role?: string
  avatar_url?: string
  is_active?: boolean
}

export const userService = {
  async getAllUsers(): Promise<User[]> {
    const response = await apiClient.get('/users/')
    return response.data
  },

  async getUser(userId: number): Promise<User> {
    const response = await apiClient.get(`/users/${userId}`)
    return response.data
  },

  async updateUser(userId: number, data: UserUpdateData): Promise<User> {
    const response = await apiClient.patch(`/users/${userId}`, data)
    return response.data
  },

  async deleteUser(userId: number): Promise<void> {
    await apiClient.delete(`/users/${userId}`)
  }
}
