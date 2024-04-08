import { type InjectionKey } from 'vue'
import { createStore, Store, useStore as baseUseStore } from 'vuex'
import { type User } from '@/types'

interface State {
  user: User | null
}

export const key: InjectionKey<Store<State>> = Symbol()

export const userStore = createStore<State>({
  state: {
    user: null
  },

  getters: {
    fullName: (state) => `${state.user!.first_name} ${state.user!.last_name}`,
    email: (state) => state.user!.email,
    isAdmin: (state) => state.user!.roles.includes('admin'),
    isLibrarian: (state) => state.user!.roles.includes('librarian'),
    isUser: (state) => state.user!.roles.includes('user'),
    isAuth: (state) => !!state.user,
    authToken: (state) => state.user!.authentication_token,
    userId: (state) => state.user!.id,
    role: (state) => state.user!.roles[0].toLocaleUpperCase(),
    user: (state) => state.user
  },

  mutations: {
    SET_USER(state, user: User) {
      state.user = user
    }
  },

  actions: {
    login({ commit }, user: User) {
      localStorage.setItem('user', JSON.stringify(user))
      commit('SET_USER', user)
    },
    logout({ commit }) {
      localStorage.removeItem('user')
      commit('SET_USER', null)
    },
    checkAuth({ commit }) {
      const user = JSON.parse(localStorage.getItem('user') || 'null')
      commit('SET_USER', user)
    }
  }
})

export const useStore = () => baseUseStore(key)
