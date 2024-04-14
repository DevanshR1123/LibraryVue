<script setup lang="ts">
import { useStore } from '@/store'
import { type LoginResponse, type User } from '@/types'
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { toast } from 'vue3-toastify'

const router = useRouter()

const store = useStore()
const isAuth = computed(() => store.getters.isAuth)

const email = ref('')
const password = ref('')
const errors = ref<string[]>([])
const loading = ref(false)

const login = async () => {
  loading.value = true
  const userCreds = { email: email.value, password: password.value }
  const res: LoginResponse = await fetch('http://localhost:5000/login?include_auth_token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userCreds)
  }).then((res: Response) => res.json())

  if (res.meta.code === 200 && 'user' in res.response) {
    store.dispatch('login', res.response.user)
    email.value = ''
    password.value = ''
    router.push('/')
  } else if (res.meta.code === 400 && 'errors' in res.response) {
    errors.value = res.response.errors
    password.value = ''
  }

  loading.value = false
}

onMounted(() => {
  if (isAuth.value) router.push('/')
})
</script>

<template>
  <section class="login">
    <h1>Login</h1>
    <form @submit.prevent="login">
      <label for="email"
        >Email
        <input type="email" id="email" v-model="email" required />
      </label>
      <label for="password"
        >Password
        <input type="password" id="password" v-model="password" required />
      </label>
      <div class="error" v-if="errors.length">
        <p v-for="error in errors" :key="error">{{ error }}!</p>
      </div>
      <button type="submit" :disabled="loading">
        Login
        <div class="loader" v-if="loading"></div>
      </button>
    </form>
  </section>
</template>

<style scoped>
.login {
  padding: 2rem;
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;

  background-color: var(--color-background-mute);

  place-self: center;

  display: grid;
  gap: 2rem;

  min-width: 24rem;
  width: fit-content;
}

h1 {
  text-align: center;
  font-weight: bold;
  font-size: 2.5rem;
}

form {
  display: grid;
  gap: 1rem;
}

label {
  display: grid;
  gap: 0.25rem;

  font-size: 0.9rem;
}

input {
  padding: 0.75em;
  border: 1px solid var(--color-border);
  border-radius: 0.25rem;

  font-size: 1rem;
}

button {
  margin-top: 1rem;
  padding: 0.5rem;
  border: none;
  border-radius: 0.25rem;

  font-size: 1.25rem;
  font-weight: bold;

  cursor: pointer;

  transition: background-color 500ms;
  background-color: var(--color-primary);
  color: var(--color-background);

  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;

  &:hover {
    background-color: var(--color-primary-dark);
  }

  &:disabled {
    background-color: var(--color-primary-dark);
    cursor: not-allowed;
  }
}

.error {
  font-size: 0.9rem;
  color: var(--color-error);
}

.loader {
  border-color: var(--color-background) transparent var(--color-background) transparent;
  width: 1em;
  margin: 0;
}
</style>
