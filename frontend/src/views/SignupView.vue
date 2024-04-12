<script setup lang="ts">
import { useStore } from '@/store'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const store = useStore()
const isAuth = computed(() => store.getters.isAuth)

const firstName = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const errors = ref<string[]>([])
const loading = ref(false)

const router = useRouter()

const signup = async () => {
  loading.value = true
  if (password.value !== confirmPassword.value) {
    alert('Passwords do not match')
    return
  }

  const user = {
    first_name: firstName.value,
    last_name: lastName.value,
    email: email.value,
    password: password.value,
    confirm_password: confirmPassword.value
  }

  const res = await fetch('http://localhost:5000/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user)
  })

  if (res.ok) router.push('/login')

  loading.value = false
}

onMounted(() => {
  if (isAuth.value) router.push('/')
})
</script>

<template>
  <section class="signup">
    <h1>Signup</h1>
    <form @submit.prevent="signup">
      <label for="first-name"
        >First Name
        <input type="text" id="first-name" v-model.trim="firstName" required />
      </label>

      <label for="last-name"
        >Last Name
        <input type="text" id="last-name" v-model.trim="lastName" required />
      </label>

      <label for="email"
        >Email
        <input type="email" id="email" v-model="email" required />
      </label>

      <label for="password"
        >Password
        <input type="password" id="password" v-model="password" required />
      </label>

      <label for="confirm-password"
        >Confirm Password
        <input type="password" id="confirm-password" v-model="confirmPassword" required />
      </label>

      <div class="error" v-if="errors.length">
        <p v-for="error in errors" :key="error">{{ error }}!</p>
      </div>

      <button type="submit" :disabled="loading">
        Signup
        <div class="loader" v-if="loading"></div>
      </button>
    </form>
  </section>
</template>

<style scoped>
.signup {
  padding: 2rem;
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;

  background-color: var(--color-background-mute);

  place-self: center;

  display: grid;
  gap: 2rem;

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

  grid-template-columns: repeat(2, 1fr);

  & > :nth-child(3) {
    grid-column: 1 / -1;
  }
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
  grid-column: 1 / -1;

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

.loader {
  border-color: var(--color-background) transparent var(--color-background) transparent;
  width: 1em;
  margin: 0;
}
</style>
