<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useStore } from '@/store'
import { useRouter } from 'vue-router'
import { computed } from 'vue'

const router = useRouter()

const store = useStore()
const fullName = computed(() => store.getters.fullName)
const isAuth = computed(() => store.getters.isAuth)
const logoutAction = () => store.dispatch('logout')

const logout = () => {
  logoutAction()
  router.push('/login')
}
</script>

<template>
  <div class="auth" v-if="isAuth">
    <div>
      Hello, <span class="name">{{ fullName }}</span>
    </div>
    <button class="logout-btn btn" @click="logout">Logout</button>
  </div>
  <div class="auth" v-else>
    <RouterLink class="login-btn btn" to="/login">Login</RouterLink>
    <RouterLink class="signup-btn btn" to="/signup">Signup</RouterLink>
  </div>
</template>

<style scoped>
.auth {
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: flex-end;
}

.name {
  font-weight: bold;
}

.btn {
  padding: 0.5em 1em;
  border: none;
  border-radius: 0.5em;
  text-decoration: none;
  font-weight: bold;

  transition: all 200ms;
  cursor: pointer;

  font-size: 1rem;
}

.login-btn,
.logout-btn {
  background-color: var(--color-primary);
  color: var(--color-background);

  border: 2px solid var(--color-primary);

  &:hover {
    background-color: var(--color-primary-light);
    color: var(--color-secondary);
  }
}

.signup-btn {
  background-color: var(--color-background-soft);
  color: var(--color-secondary);

  border: 2px solid var(--color-secondary);

  &:hover {
    background-color: var(--color-secondary);
    color: var(--color-background);
  }
}
</style>
