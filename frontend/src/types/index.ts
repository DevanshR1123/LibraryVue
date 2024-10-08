export interface User {
  id: number
  firstname: string
  lastname: string
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

export interface NewSection {
  name: string
  description: string
  image: string | File | null
}

export interface Section {
  id: number
  name: string
  description: string
  image: string | File | null
  books: Book[]
}

export interface NewBook {
  title: string
  author: string
  description: string
  isbn: string
  year: number
  content: string | File | null
  image: string | File | null
  section_id: number
}

export interface Book {
  id: number
  title: string
  author: string
  description: string
  isbn: string
  year: number
  image: string | File | null
  date_added: Date
  section: Section
  rating: number
  comments: Comment[]
  issued: boolean
}

export interface Comment {
  id: number
  user_id: number
  book_id: number
  content: string
  timestamp: Date
  username: string
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
  request_date: Date
  issue_date: Date
  return_date: Date
  returned: boolean
  granted: boolean
  active: boolean
  requested: boolean
}

export interface LibrarianIssue extends BookIssue {
  user: User
  book: Book
}

export interface LibraryStats {
  total_users: number
  total_books: number
  total_issued: number
  total_sections: number
  total_years: number
  sections: Record<string, number>
  years: Record<number, number>
  issued_books: Record<string, number>
  percentage_issued: number
  top_5_most_issued_sections: Array<{ section: string; total_issues: number }>
  top_5_most_issued_books: Array<{ title: string; total_issues: number }>
}

export interface UserStats {
  total_issues: number
  total_books: number
  total_sections: number
  sections: Record<string, number>
  top_5_most_issued_sections: Array<{ section: string; count: number }>
  top_5_most_issued_books: Array<{ title: string; count: number }>
}
