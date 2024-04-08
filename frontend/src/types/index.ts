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
  id: number
  name: string
  description: string
  image: string
  books: Book[]
}

export interface Book {
  id: number
  title: string
  author: string
  description: string
  isbn: string
  year: number
  content: string
  image: string
  date_added: Date
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
