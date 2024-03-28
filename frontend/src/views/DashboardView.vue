<script setup lang="ts">
import { useStore } from '@/store'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const store = useStore()
const isAuth = computed(() => store.getters.isAuth)
const fullName = computed(() => store.getters.fullName)

const router = useRouter()

if (!isAuth.value) {
  router.push('/login')
}

const logout = () => {
  store.dispatch('logout')
  router.push('/login')
}
</script>

<template>
  <section class="dashboard">
    <h1>Dashboard</h1>
    <p>Welcome, {{ fullName }}</p>
    <button @click="logout">Logout</button>
  </section>
</template>

<style scoped>
.dashboard {
  padding: 2rem;
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;

  background-color: var(--color-background-mute);
}

.dashboard button {
  margin-top: 1rem;
}

.dashboard p {
  font-size: 1.25rem;
}

.dashboard h1 {
  text-align: center;
  font-weight: bold;
  font-size: 2.5rem;
}

.dashboard button {
  padding: 0.5rem;
  border: none;
  border-radius: 0.25rem;

  font-size: 1.25rem;
  font-weight: bold;

  cursor: pointer;

  transition: background-color 500ms;
}

.dashboard button:hover {
  background-color: var(--color-background-mute-hover);
}
</style>
