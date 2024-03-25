<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import Logo from '@/components/AppLogo.vue'

const links = [
  { path: '/', name: 'Home' },
  { path: '/about', name: 'About' }
]
</script>

<template>
  <header>
    <h1>
      <Logo />
      LibraryMS
    </h1>
    <nav>
      <ul class="nav-links">
        <li v-for="link in links" :key="link.path">
          <RouterLink :to="link.path">{{ link.name }}</RouterLink>
        </li>
      </ul>
    </nav>
    <div class="auth">
      <RouterLink class="login-btn btn" to="/login">Login</RouterLink>
      <RouterLink class="signup-btn btn" to="/signup">Signup</RouterLink>
    </div>
  </header>
  <main>
    <RouterView />
  </main>
</template>
<style scoped>
header {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  background-color: var(--color-background-mute);
  color: var(--color-text);
  padding: 1rem;
  gap: 2rem;
}

h1 {
  display: flex;
  align-items: center;
  gap: 0.5rem;

  font-weight: 900;
}

nav {
  width: 100%;
  text-align: center;

  & ul {
    list-style: none;
    padding: 0;
    display: flex;
    justify-content: center;
    gap: 2rem;
  }

  & a {
    color: var(--color-text);
    display: inline-block;
    padding: 0 0.25em;
    text-decoration: none;
    font-weight: bold;

    transition: color 500ms;

    &:hover {
      color: var(--color-primary);
    }

    &::after {
      content: '';
      display: block;
      position: absolute;
      inset: auto 0 -0.1em;
      height: 0.15em;

      background-color: var(--color-primary);

      opacity: 0;
      transition: opacity 500ms;
    }

    &.router-link-exact-active {
      color: var(--color-primary);
      position: relative;

      &::after {
        opacity: 1;
      }
    }
  }
}

.auth {
  display: flex;
  gap: 1rem;

  & .btn {
    padding: 0.25em 1em;
    border: none;
    border-radius: 0.5em;
    text-decoration: none;
    font-weight: bold;

    transition: all 250ms;
  }

  & .login-btn {
    background-color: var(--color-primary);
    color: var(--color-background);

    border: 2px solid var(--color-primary);

    &:hover {
      background-color: var(--color-background-soft);
      color: var(--color-secondary);
    }
  }

  & .signup-btn {
    background-color: var(--color-background-soft);
    color: var(--color-secondary);

    border: 2px solid var(--color-secondary);

    &:hover {
      background-color: var(--color-secondary);
      color: var(--color-background);
    }
  }
}

main {
  padding: 1rem;
  display: grid;
}
</style>
