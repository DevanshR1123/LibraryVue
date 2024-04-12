import { type InjectionKey } from 'vue'
import { createStore, Store, useStore as baseUseStore } from 'vuex'
import { type User, type Book, type Section } from '@/types'

interface State {
  user: User | null
  books: Book[]
  sections: Section[]
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
    sections: []
  },

  getters: {
    // User
    isAuth: (state) => !!state.user,
    fullName: (state) => `${state.user!.first_name} ${state.user!.last_name}`,
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
    section: (state) => (id: number) => state.sections.find((section: Section) => section.id === id)
  },

  mutations: {
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
    }
  },

  actions: {
    // User
    login({ commit }, user: User) {
      localStorage.setItem('user', JSON.stringify(user))
      commit('SET_USER', user)
    },
    logout({ commit }) {
      localStorage.removeItem('user')
      commit('SET_USER', null)
    },
    async checkAuth({ commit }) {
      const user = JSON.parse(localStorage.getItem('user') || 'null')
      const token = user ? user.authentication_token : null
      if (token) {
        const res = await fetch(`${apiUrl}/check-auth`, {
          headers: { ...headers, 'Authentication-Token': token }
        })

        if (res.status === 200) {
          commit('SET_USER', user)
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

    // Sections
    async getSections({ commit }) {
      const response = await fetch(`${apiUrl}/sections`, { headers })
      const data = await response.json()
      commit('SET_SECTIONS', data)
    }
  }
})

export const useStore = () => baseUseStore(key)
