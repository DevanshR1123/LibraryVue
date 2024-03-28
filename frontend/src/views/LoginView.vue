<script setup lang="ts">
import { useStore } from '@/store'
import { type LoginResponse, type User } from '@/types'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const store = useStore()
const isAuth = store.getters.isAuth
const loginAction = (user: User) => store.dispatch('login', user)

if (isAuth) {
  router.push('/')
}

const email = ref('')
const password = ref('')

const login = async () => {
  const user = { email: email.value, password: password.value }
  const res: LoginResponse = await fetch('http://localhost:5000/login?include_auth_token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user)
  }).then((res: Response) => res.json())

  if (res.meta.code === 200) {
    loginAction(res.response.user)
    router.push('/')
  }
}
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
      <button type="submit">Login</button>
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

  margin-bottom: 10vh;

  width: 24rem;
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
  margin-top: 2rem;
  padding: 0.5rem;
  border: none;
  border-radius: 0.25rem;

  font-size: 1.25rem;
  font-weight: bold;

  cursor: pointer;

  transition: background-color 500ms;
  background-color: var(--color-primary);
  color: var(--color-background);

  &:hover {
    background-color: var(--color-primary-dark);
  }
}
</style>
