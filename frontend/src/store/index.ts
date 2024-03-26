import { type InjectionKey } from 'vue'
import { createStore, Store, useStore as baseUseStore } from 'vuex'
import { type User } from '@/types'

interface State {
  user: User | null
}

export const key: InjectionKey<Store<State>> = Symbol()

export const userStore = createStore({
  state: {
    user: {
      id: 1,
      firstName: 'John',
      lastName: 'Doe',
      email: 'john.doe@example.com',
      role: 'admin'
    }
  },

  getters: {
    fullName: (state) => `${state.user.firstName} ${state.user.lastName}`,
    email: (state) => state.user.email,
    isAdmin: (state) => state.user.role === 'admin',
    isLibrarian: (state) => state.user.role === 'librarian',
    isUser: (state) => state.user.role === 'user',
    isAuth: (state) => !!state.user
  },

  mutations: {
    SET_USER(state, user: User) {
      state.user = user
    }
  },

  actions: {
    login({ commit }, user: User) {
      commit('SET_USER', user)
    },
    logout({ commit }) {
      commit('SET_USER', null)
    }
  }
})

export const useStore = () => baseUseStore(key)
