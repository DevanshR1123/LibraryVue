export interface User {
  id: number
  first_name: string
  last_name: string
  email: string
  roles: string[]
  authentication_token: string
}

export interface LoginResponse {
  meta: { code: number }
  response: {
    user: User
  }
}
