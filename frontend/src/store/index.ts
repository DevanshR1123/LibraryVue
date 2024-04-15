import { type InjectionKey } from 'vue'
import { createStore, Store, useStore as baseUseStore } from 'vuex'
import type { User, Book, NewBook, Section, NewSection, BookIssue, LibrarianIssue, Rating } from '@/types'
import { toast } from 'vue3-toastify'

interface State {
  user: User | null
  books: Book[]
  sections: Section[]
  issues: BookIssue[] | LibrarianIssue[]
  ratings: Rating[]
}

const apiUrl = 'http://localhost:5000'
const headers = {
  'Content-Type': 'application/json'
}

export const key: InjectionKey<Store<State>> = Symbol()

export const store = createStore<State>({
  state: {
    user: null,
    books: [],
    sections: [],
    issues: [],
    ratings: []
  },

  getters: {
    // User
    isAuth: (state) => !!state.user,
    fullName: (state) => `${state.user!.firstname} ${state.user!.lastname}`,
    email: (state) => state.user!.email,
    isAdmin: (state) => state.user?.roles.length && state.user!.roles.includes('admin'),
    isLibrarian: (state) => state.user?.roles.length && state.user!.roles.includes('librarian'),
    isUser: (state) => state.user?.roles.length && state.user!.roles.includes('user'),
    authToken: (state) => state.user!.authentication_token,

    // Books
    books: (state) => state.books,
    book: (state) => (id: number) => state.books.find((book: Book) => book.id === id),

    // Sections
    sections: (state) => state.sections,
    section: (state) => (id: number) => state.sections.find((section: Section) => section.id === id),

    // Issues
    issues: (state) => state.issues,

    issued: (state) => (book_id: number) => state.issues.some((issue) => issue.book_id === book_id && issue.active),
    requested: (state) => (book_id: number) =>
      state.issues.some((issue) => issue.book_id === book_id && issue.requested),

    active_issues: (state) => state.issues.filter((issue) => issue.active),
    issue_requests: (state) => state.issues.filter((issue) => issue.requested),

    active_issues_by_book: (state) => (book_id: number) =>
      state.issues.filter((issue) => issue.book_id === book_id && issue.active),
    issue_requests_by_book: (state) => (book_id: number) =>
      state.issues.filter((issue) => issue.book_id === book_id && issue.requested),

    // Ratings
    ratings: (state) => state.ratings,
    rating: (state) => (book_id: number) => state.ratings.find((rating: Rating) => rating.book_id === book_id)
  },

  mutations: {
    CLEAR_STATE(state) {
      state.user = null
      state.books = []
      state.sections = []
      state.issues = []
      state.ratings = []
    },

    CLEAR_USER_DATA(state) {
      state.user = null
      state.issues = []
      state.ratings = []
    },

    // User
    SET_USER(state, user: User) {
      state.user = user
    },

    // Books
    SET_BOOKS(state, books: Book[]) {
      state.books = books
    },

    // Sections
    SET_SECTIONS(state, sections: Section[]) {
      state.sections = sections
    },

    // Issues
    SET_ISSUES(state, issues: BookIssue[] | LibrarianIssue[]) {
      state.issues = issues
    },

    // Ratings
    SET_RATINGS(state, ratings: Rating[]) {
      state.ratings = ratings
    }
  },

  actions: {
    // User
    login({ commit, dispatch, getters }, user: User) {
      localStorage.setItem('user', JSON.stringify(user))
      commit('SET_USER', user)

      toast.success(`Welcome back, ${getters.fullName}`)

      if (getters.isUser) {
        dispatch('getIssues')
        dispatch('getRatings')
      } else if (getters.isLibrarian) {
        dispatch('getLibrarianIssues')
      }
    },

    logout({ commit }) {
      localStorage.removeItem('user')
      commit('CLEAR_USER_DATA')
    },

    async checkAuth({ commit, dispatch, getters }) {
      const user = JSON.parse(localStorage.getItem('user') || 'null')
      const token = user ? user.authentication_token : null
      if (token) {
        const res = await fetch(`${apiUrl}/check-auth`, {
          headers: { ...headers, 'Authentication-Token': token }
        })

        if (res.status === 200) {
          commit('SET_USER', user)
          if (getters.isUser) {
            dispatch('getIssues')
            dispatch('getRatings')
          } else if (getters.isLibrarian) {
            dispatch('getLibrarianIssues')
          }
        } else {
          localStorage.removeItem('user')
          commit('SET_USER', null)
        }
      }
    },

    // Books
    async getBooks({ commit }) {
      const response = await fetch(`${apiUrl}/books`, { headers })
      const data = await response.json()
      commit('SET_BOOKS', data)
    },

    async createBook({ dispatch, state, getters }, book: NewBook) {
      const bookData = new FormData()
      bookData.append('title', book.title)
      bookData.append('author', book.author)
      bookData.append('description', book.description)
      bookData.append('isbn', book.isbn)
      bookData.append('year', book.year.toString())

      if (!book.section_id) throw new Error('No section selected')
      bookData.append('section_id', book.section_id.toString())
      if (!book.content) throw new Error('No content provided')
      bookData.append('content', book.content)
      if (book.image) bookData.append('image', book.image)

      if (!state.user || !(getters.isAdmin || getters.isLibrarian)) return

      const response = await fetch(`${apiUrl}/books`, {
        method: 'POST',
        headers: { 'Authentication-Token': state.user.authentication_token },
        body: bookData
      })

      if (response.status === 201) {
        dispatch('getBooks')
        toast.success('Book created successfully')
      }
    },

    async updateBook({ dispatch, state, getters }, { book_id, book }: { book_id: number; book: NewBook }) {
      const bookData = new FormData()
      bookData.append('title', book.title)
      bookData.append('author', book.author)
      bookData.append('description', book.description)
      bookData.append('isbn', book.isbn)
      bookData.append('year', book.year.toString())

      if (!book.section_id) throw new Error('No section selected')
      bookData.append('section_id', book.section_id.toString())
      if (book.content) bookData.append('content', book.content)
      if (book.image) bookData.append('image', book.image)

      if (!state.user || !(getters.isAdmin || getters.isLibrarian)) return

      const response = await fetch(`${apiUrl}/books/${book_id}`, {
        method: 'PUT',
        headers: { 'Authentication-Token': state.user.authentication_token },
        body: bookData
      })

      if (response.status === 201) {
        dispatch('getBooks')
        toast.success('Book updated successfully')
      }
    },

    async deleteBook({ dispatch, state, getters }, book_id: number) {
      if (!state.user || !(getters.isAdmin || getters.isLibrarian)) return

      const response = await fetch(`${apiUrl}/books/${book_id}`, {
        method: 'DELETE',
        headers: { 'Authentication-Token': state.user.authentication_token }
      })

      if (response.status === 204) {
        dispatch('getBooks')
        toast.success('Book deleted successfully')
      }
    },

    // Sections
    async getSections({ commit }) {
      const response = await fetch(`${apiUrl}/sections`, { headers })
      const data = await response.json()
      commit('SET_SECTIONS', data)
    },

    async createSection({ dispatch, state, getters }, section: NewSection) {
      const sectionData = new FormData()
      sectionData.append('name', section.name)
      sectionData.append('description', section.description)
      if (section.image) {
        sectionData.append('image', section.image)
      }

      if (!state.user || !(getters.isAdmin || getters.isLibrarian)) return

      const response = await fetch(`${apiUrl}/sections`, {
        method: 'POST',
        headers: { 'Authentication-Token': state.user.authentication_token },
        body: sectionData
      })

      if (response.status === 201) {
        dispatch('getSections')
        toast.success('Section created successfully')
      }
    },

    async updateSection(
      { dispatch, state, getters },
      { section_id, section }: { section_id: number; section: NewSection }
    ) {
      const sectionData = new FormData()
      sectionData.append('name', section.name)
      sectionData.append('description', section.description)
      if (section.image) {
        sectionData.append('image', section.image)
      }

      if (!state.user || !(getters.isAdmin || getters.isLibrarian)) return

      const response = await fetch(`${apiUrl}/sections/${section_id}`, {
        method: 'PUT',
        headers: { 'Authentication-Token': state.user.authentication_token },
        body: sectionData
      })

      if (response.status === 201) {
        dispatch('getSections')
        toast.success('Section updated successfully')
      }
    },

    async deleteSection({ dispatch, state, getters }, section_id: number) {
      if (!state.user || !(getters.isAdmin || getters.isLibrarian)) return
      const response = await fetch(`${apiUrl}/sections/${section_id}`, {
        method: 'DELETE',
        headers: { 'Authentication-Token': state.user.authentication_token }
      })

      if (response.status === 204) {
        dispatch('getSections')
        toast.success('Section deleted successfully')
      }
    },

    // Issues
    async getIssues({ commit, state }) {
      if (!state.user) return
      const response = await fetch(`${apiUrl}/issues`, {
        headers: { 'Authentication-Token': state.user.authentication_token }
      })
      const data = (await response.json()) as BookIssue[]
      commit('SET_ISSUES', data)
    },

    async issueBook({ dispatch, state }, book_id: number) {
      if (!state.user) return
      const response = await fetch(`${apiUrl}/issues/${book_id}`, {
        method: 'POST',
        headers: { 'Authentication-Token': state.user.authentication_token }
      })

      if (response.status === 201) {
        dispatch('getIssues')
        toast.success('Book requested successfully')
      } else if (response.status === 400) {
        const { message } = await response.json()
        toast.error(message)
      }
    },

    async unissueBook({ dispatch, state }, book_id: number) {
      if (!state.user) return
      const response = await fetch(`${apiUrl}/issues/${book_id}`, {
        method: 'PUT',
        headers: { 'Authentication-Token': state.user.authentication_token }
      })

      if (response.status === 201) {
        dispatch('getIssues')
        toast.success('Book unissued successfully')
      }
    },

    async returnBook({ dispatch, state }, book_id: number) {
      if (!state.user) return
      const response = await fetch(`${apiUrl}/issues/${book_id}`, {
        method: 'DELETE',
        headers: { 'Authentication-Token': state.user.authentication_token }
      })

      if (response.status === 204) {
        dispatch('getIssues')
        toast.success('Book returned successfully')
      }
    },

    // Ratings

    async getRatings({ commit, state }) {
      if (!state.user) return
      const response = await fetch(`${apiUrl}/ratings`, {
        headers: { 'Authentication-Token': state.user.authentication_token }
      })
      const data = await response.json()
      commit('SET_RATINGS', data)
    },

    async rateBook({ dispatch, state }, { book_id, rating }) {
      if (!state.user) return
      const response = await fetch(`${apiUrl}/ratings${book_id}`, {
        method: 'POST',
        headers: { ...headers, 'Authentication-Token': state.user.authentication_token },
        body: JSON.stringify({ rating })
      })

      if (response.status === 201) {
        dispatch('getBooks')
        dispatch('getRatings')
      }
    },

    // Librarian actions

    async getLibrarianIssues({ commit, state, getters }) {
      if (!state.user || !getters.isLibrarian) return
      const response = await fetch(`${apiUrl}/librarian/issues`, {
        headers: { ...headers, 'Authentication-Token': state.user.authentication_token }
      })
      const data = (await response.json()) as LibrarianIssue[]
      commit('SET_ISSUES', data)
    },

    async grantBook({ dispatch, state, getters }, issue_id: number) {
      if (!state.user || !getters.isLibrarian) return
      const response = await fetch(`${apiUrl}/librarian/issues/${issue_id}`, {
        method: 'POST',
        headers: { 'Authentication-Token': state.user.authentication_token }
      })

      if (response.status === 201) {
        dispatch('getBooks')
        dispatch('getLibrarianIssues')
        toast.success('Book granted successfully')
      }
    },

    async rejectBook({ dispatch, state, getters }, issue_id: number) {
      if (!state.user || !getters.isLibrarian) return
      const response = await fetch(`${apiUrl}/librarian/issues/${issue_id}`, {
        method: 'PUT',
        headers: { 'Authentication-Token': state.user.authentication_token }
      })

      if (response.status === 201) {
        dispatch('getBooks')
        dispatch('getLibrarianIssues')
        toast.success('Book rejected successfully')
      }
    },

    async revokeBook({ dispatch, state, getters }, issue_id: number) {
      if (!state.user || !(getters.isAdmin || getters.isLibrarian)) return

      const response = await fetch(`${apiUrl}/librarian/issues/${issue_id}`, {
        method: 'DELETE',
        headers: { 'Authentication-Token': state.user.authentication_token }
      })

      if (response.status === 204) {
        dispatch('getBooks')
        dispatch('getLibrarianIssues')
        toast.success('Book revoked successfully')
      }
    }
  }
})

export const useStore = () => baseUseStore(key)
