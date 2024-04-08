import { type Book, type Section } from '@/types'
// import { userStore } from '@/store'

const apiUrl = 'http://localhost:5000'
const headers = {
  'Content-Type': 'application/json'
}

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
  const response = await fetch(`${apiUrl}/books`, {
    method: 'POST',
    headers,
    body: JSON.stringify(book)
  })
  const data = await response.json()
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
