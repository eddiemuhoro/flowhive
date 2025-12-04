export interface User {
  id: number
  email: string
  username: string
  full_name?: string
  role: UserRole
  avatar_url?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export enum UserRole {
  TEAM_MEMBER = 'team_member',
  MANAGER = 'manager',
  EXECUTIVE = 'executive'
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
  full_name?: string
  role?: UserRole
}

export interface AuthResponse {
  access_token: string
  token_type: string
}
