<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import Logo from '@/components/AppLogo.vue'
import NavAuth from '@/components/NavAuth.vue'
import { useStore } from '@/store'
import { computed, onBeforeMount } from 'vue'

const store = useStore()
const isAuth = computed(() => store.getters.isAuth)

const baseLinks = [
  { path: '/', name: 'Home' },
  // { path: '/about', name: 'About' },
  { path: '/books', name: 'Books' },
  { path: '/sections', name: 'Sections' }
]

const authLinks = [{ path: '/dashboard', name: 'Dashboard' }]
const links = computed(() => (isAuth.value ? [...baseLinks, ...authLinks] : baseLinks))

onBeforeMount(() => {
  store.dispatch('checkAuth')
  store.dispatch('getBooks')
  store.dispatch('getSections')
})
</script>

<template>
  <header>
    <RouterLink to="/">
      <h1>
        <Logo />
        LibraryVue
      </h1>
    </RouterLink>

    <nav>
      <ul class="nav-links">
        <li v-for="link in links" :key="link.path">
          <RouterLink :to="link.path">{{ link.name }}</RouterLink>
        </li>
      </ul>
    </nav>
    <NavAuth />
  </header>
  <main>
    <RouterView v-slot="{ Component }">
      <template v-if="Component">
        <KeepAlive>
          <Suspense>
            <component :is="Component"></component>
            <template #fallback> <div class="loader"></div> </template>
          </Suspense>
        </KeepAlive>
      </template>
    </RouterView>
  </main>
</template>
<style scoped>
header {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  background-color: var(--color-background-mute);
  color: var(--color-text);
  padding: 1rem;
  gap: 2rem;

  position: sticky;
  top: 0;

  z-index: 1000;

  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1);
}

h1 {
  display: flex;
  align-items: center;
  gap: 0.5rem;

  font-weight: 900;
}

a {
  color: var(--color-text);
  text-decoration: none;
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
</style>
