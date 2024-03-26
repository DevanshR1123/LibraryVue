<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from '@/store'
import { type User } from '@/types'

const router = useRouter()

const store = useStore()
const isAuth = store.getters.isAuth
const loginAction = (user: User) => store.dispatch('login', user)

if (isAuth) {
  router.push('/')
}

const email = ref('')
const password = ref('')

const login = () => {
  console.log('Login', email.value, password.value)
  loginAction({
    id: 1,
    firstName: 'John',
    lastName: 'Doe',
    email: 'john.doe@example.com',
    role: 'admin'
  })
  router.push('/')
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
