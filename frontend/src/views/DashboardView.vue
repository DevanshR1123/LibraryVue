<script setup lang="ts">
import { useStore } from '@/store'
import { computed, Suspense } from 'vue'
import { useRouter } from 'vue-router'

import AdminDashboard from '@/components/dashboard/AdminDashboard.vue'
import LibrarianDashboard from '@/components/dashboard/LibrarianDashboard.vue'
import UserDashboard from '@/components/dashboard/UserDashboard.vue'

const store = useStore()
const isAuth = computed(() => store.getters.isAuth)

const isAdmin = computed(() => store.getters.isAdmin)
const isLibrarian = computed(() => store.getters.isLibrarian)
const isUser = computed(() => store.getters.isUser)

const fullName = computed(() => store.getters.fullName)

const router = useRouter()

if (!isAuth.value) {
  router.push('/login')
}
</script>

<template>
  <div class="dashboard-view">
    <section class="dashboard-header">
      <h1>Dashboard</h1>
      <p>Welcome, {{ fullName }}</p>
    </section>
    <Suspense>
      <LibrarianDashboard v-if="isLibrarian" />
      <UserDashboard v-else-if="isUser" />
      <AdminDashboard v-else-if="isAdmin" />
    </Suspense>
  </div>
</template>

<style scoped>
.dashboard-view {
  display: grid;
  gap: 1rem;

  grid-template-rows: auto 1fr;
}

.dashboard-header {
  padding: 1rem 2rem;
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;

  & button {
    margin-top: 1rem;
  }

  & p {
    font-size: 1.25rem;
  }

  & h1 {
    text-align: center;
    font-weight: bold;
    font-size: 2.5rem;
  }

  & button {
    padding: 0.5rem;
    border: none;
    border-radius: 0.25rem;

    font-size: 1.25rem;
    font-weight: bold;

    cursor: pointer;

    transition: background-color 500ms;
  }
}
</style>
