import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import DashboardView from '@/views/DashboardView.vue'
import BooksView from '@/views/BooksView.vue'
import BookView from '@/views/BookView.vue'
import AuthorsView from '@/views/AuthorsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        requiresAuth: false,
        title: 'Home'
      }
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
      meta: {
        requiresAuth: false,
        title: 'About'
      }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: {
        requiresAuth: false,
        title: 'Login'
      }
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
      meta: {
        requiresAuth: false,
        title: 'Signup'
      }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: {
        requiresAuth: true,
        title: 'Dashboard'
      }
    },
    {
      path: '/books',
      name: 'books',
      component: BooksView,
      meta: {
        requiresAuth: true,
        title: 'Books'
      }
    },
    {
      path: '/books/:id',
      name: 'book',
      component: BookView,
      meta: { requiresAuth: true },
      props: true
    },
    {
      path: '/authors',
      name: 'authors',
      component: AuthorsView,
      meta: {
        requiresAuth: true,
        title: 'Authors'
      }
    }
  ]
})

router.afterEach((to) => {
  document.title = to.meta.title ? `LibraryVue | ${to.meta.title}` : 'LibraryVue'
})

export default router
