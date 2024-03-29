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

export interface Book {
  id: number
  title: string
  author: string
  genre: string
  year: number
  description: string
  image: string
}
