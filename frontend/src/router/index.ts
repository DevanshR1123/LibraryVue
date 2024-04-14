import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import DashboardView from '@/views/DashboardView.vue'
import BooksView from '@/views/BooksView.vue'
import BookView from '@/views/BookView.vue'
import SectionsView from '@/views/SectionsView.vue'
import SectionView from '@/views/SectionView.vue'
import SearchView from '@/views/SearchView.vue'
import ReaderView from '@/views/ReaderView.vue'
import IssueManagement from '@/components/dashboard/librarian/IssueManagement.vue'
import LibrarianDashboard from '@/components/dashboard/librarian/LibrarianDashboard.vue'
import BooksManagement from '@/components/dashboard/librarian/BooksManagement.vue'
import SectionManagement from '@/components/dashboard/librarian/SectionManagement.vue'

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
      },
      children: [
        {
          path: '',
          name: 'librarian-dashboard',
          component: LibrarianDashboard
        },
        {
          path: 'issues',
          name: 'issue-management',
          component: IssueManagement
        },
        {
          path: 'books',
          name: 'librarian-books',
          component: BooksManagement
        },
        {
          path: 'sections',
          name: 'librarian-sections',
          component: SectionManagement
        }
      ]
    },
    {
      path: '/books',
      name: 'books',
      component: BooksView,
      meta: { requiresAuth: true }
    },
    {
      path: '/books/:id',
      name: 'book',
      component: BookView,
      meta: {
        requiresAuth: true,
        title: 'Books'
      },
      props: true
    },
    {
      path: '/sections',
      name: 'sections',
      component: SectionsView,
      meta: {
        requiresAuth: true,
        title: 'Sections'
      }
    },
    {
      path: '/sections/:id',
      name: 'section',
      component: SectionView,
      meta: { requiresAuth: true },
      props: true
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView,
      meta: {
        requiresAuth: false,
        title: 'Search'
      },
      props: true
    },
    {
      path: '/read/:id',
      name: 'read',
      component: ReaderView
    }
  ]
})

router.afterEach((to) => {
  document.title = to.meta.title ? `LibraryVue | ${to.meta.title}` : 'LibraryVue'
})

export default router
