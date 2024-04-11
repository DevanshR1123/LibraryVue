export interface User {
  id: number
  first_name: string
  last_name: string
  email: string
  roles: string[]
  authentication_token: string
}

interface LoginSuccess {
  meta: { code: 200 }
  response: { user: User }
}

interface LoginFailure {
  meta: { code: 400 }
  response: {
    errors: string[]
    field_errors: { [key: string]: string[] }
  }
}

export type LoginResponse = LoginSuccess | LoginFailure

// export interface Book {
//   id: number
//   title: string
//   author: string
//   genre: string
//   year: number
//   description: string
//   image: string
// }

export interface Section {
  id?: number
  name: string
  description: string
  image: string | File | null
  books?: Book[]
}

export interface Book {
  id?: number
  title: string
  author: string
  description: string
  isbn: string
  year: number
  content: string | File | null
  image: string | File | null
  date_added?: Date
  section_id: number
}

export interface Comment {
  id: number
  user_id: number
  book_id: number
  content: string
  timestamp: Date
}

export interface Rating {
  user_id: number
  book_id: number
  rating: number
}

export interface BookIssue {
  id: number
  user_id: number
  book_id: number
  issue_date: Date
  return_date: Date
  returned: boolean
}
