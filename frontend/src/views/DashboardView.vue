<script setup lang="ts">
import AdminToolbar from '@/components/AdminToolbar.vue'
import { useStore } from '@/store'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

// import AdminDashboard from '@/components/dashboard/AdminDashboard.vue'
// import LibrarianDashboard from '@/components/dashboard/LibrarianDashboard.vue'
// import UserDashboard from '@/components/dashboard/UserDashboard.vue'

const store = useStore()
const isAuth = computed(() => store.getters.isAuth)

// const isAdmin = computed(() => store.getters.isAdmin)
const isLibrarian = computed(() => store.getters.isLibrarian)
const isUser = computed(() => store.getters.isUser)

const router = useRouter()

// if (!isAuth.value) router.push('/login')
</script>

<template>
  <div class="dashboard-view" v-if="isAuth">
    <h1 class="dashboard-header">Dashboard</h1>

    <AdminToolbar />
    <template v-if="isLibrarian">
      <div class="dashboard-menu">
        <router-link to="/dashboard/">Library Overview</router-link>
        <router-link to="/dashboard/issues">Issue Management</router-link>
        <router-link to="/dashboard/books">Book Management</router-link>
        <router-link to="/dashboard/sections">Section Management</router-link>
      </div>
      <section class="librarian-dashboard">
        <router-view />
      </section>
    </template>

    <template v-else-if="isUser">
      <div class="dashboard-menu">
        <router-link to="/dashboard/">Profile Overview</router-link>
        <router-link to="/dashboard/issues">Active Issues</router-link>
        <router-link to="/dashboard/books">My Books</router-link>
      </div>

      <section class="user-dashboard">
        <router-view />
      </section>
    </template>
  </div>

  <div v-else class="unauthorized-view">
    <p>Please log in to view your dashboard.</p>
    <button @click="router.push('/login')">Login</button>
  </div>
</template>

<style scoped>
.dashboard-view {
  display: grid;
  gap: 1rem;

  grid-template-rows: auto auto 1fr;
  grid-template-columns: auto 1fr;
}

.librarian-dashboard {
  grid-column: 1 / -1;
}

.user-dashboard {
  grid-column: 1 / -1;
}

.dashboard-menu {
  grid-column: 1 / -1;

  list-style-type: none;
  padding: 0;

  display: flex;
  gap: 2rem;

  justify-content: center;

  & a {
    text-decoration: none;
    color: var(--color-secondary);
    font-weight: bold;

    border: 2px solid var(--color-secondary);
    border-radius: 0.5rem;
    padding: 0.5rem;

    &.router-link-exact-active {
      color: var(--color-primary-dark);
      border-color: var(--color-primary-dark);
    }
  }
}

.unauthorized-view {
  display: grid;
  gap: 1rem;
  place-content: center;
  font-size: 1.5rem;

  & button {
    padding: 0.5rem 1rem;
    border: 2px solid var(--color-primary);
    border-radius: 0.5rem;
    background-color: var(--color-primary);
    color: var(--color-background);
    font-weight: bold;

    font-size: 1.25rem;

    place-self: center;

    transition:
      background-color 500ms,
      color 500ms;

    &:hover {
      background-color: var(--color-background);
      color: var(--color-primary);
    }
  }
}
</style>
