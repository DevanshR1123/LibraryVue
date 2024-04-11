import { type Book, type Section } from '@/types'
import { store } from '@/store'

const apiUrl = 'http://localhost:5000'
const headers = {
  'Content-Type': 'application/json'
}

const authToken = () => store.getters.authToken

export const getBooks = async (): Promise<Book[]> => {
  const response = await fetch(`${apiUrl}/books`, { headers })
  const data = await response.json()
  return data
}

export const getBook = async (id: string): Promise<Book> => {
  const response = await fetch(`${apiUrl}/books/${id}`, { headers })
  const data = await response.json()
  return data
}

export const createBook = async (book: Book): Promise<Book> => {
  const bookData = new FormData()
  bookData.append('title', book.title)
  bookData.append('author', book.author)
  bookData.append('description', book.description)
  bookData.append('isbn', book.isbn)
  bookData.append('year', book.year.toString())
  bookData.append('section_id', book.section_id.toString())
  if (!book.content) throw new Error('No content provided')
  bookData.append('content', book.content)
  if (book.image) bookData.append('image', book.image)

  const response = await fetch(`${apiUrl}/books`, {
    method: 'POST',
    headers: {
      'Authentication-Token': authToken()
    },
    body: bookData
  })

  const data = (await response.json()) as Book
  return data
}

export const updateBook = async (book: Book): Promise<Book> => {
  const response = await fetch(`${apiUrl}/books/${book.id}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(book)
  })
  const data = await response.json()
  return data
}

export const deleteBook = async (id: string): Promise<void> => {
  await fetch(`${apiUrl}/books/${id}`, {
    method: 'DELETE',
    headers
  })
}

export const getSections = async (): Promise<Section[]> => {
  const response = await fetch(`${apiUrl}/sections`, { headers })
  const data = await response.json()
  return data
}

export const getSection = async (id: string): Promise<Section> => {
  const response = await fetch(`${apiUrl}/sections/${id}`, { headers })
  const data = await response.json()
  return data
}

export const createSection = async (section: Section): Promise<Section> => {
  const sectionData = new FormData()
  sectionData.append('name', section.name)
  sectionData.append('description', section.description)
  if (section.image) {
    sectionData.append('image', section.image)
  }

  const response = await fetch(`${apiUrl}/sections`, {
    method: 'POST',
    headers: {
      'Authentication-Token': authToken()
    },
    body: sectionData
  })

  const data = (await response.json()) as Section
  return data
}

export const updateSection = async (section: Section): Promise<Section> => {
  const response = await fetch(`${apiUrl}/sections/${section.id}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(section)
  })
  const data = await response.json()
  return data
}

export const deleteSection = async (id: string): Promise<void> => {
  await fetch(`${apiUrl}/sections/${id}`, {
    method: 'DELETE',
    headers
  })
}
