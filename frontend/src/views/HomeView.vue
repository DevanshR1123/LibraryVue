<script setup lang="ts">
import { useStore } from '@/store'
import { computed } from 'vue'
import SearchBox from '@/components/SearchBox.vue'
import BookCard from '@/components/books/BookCard.vue'
import SectionCard from '@/components/sections/SectionCard.vue'

const store = useStore()
const books = computed(() => store.state.books)
const sections = computed(() => store.state.sections)

const issues = computed(() => store.getters.active_issues)
</script>

<template>
  <div class="home-page">
    <div class="hero">
      <div class="app-logo">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 17" fill="currentColor">
          <path
            d="M11 2.253a1 1 0 1 0-2 0h2zm-2 13a1 1 0 1 0 2 0H9zm.447-12.167a1 1 0 1 0 1.107-1.666L9.447 3.086zM1 2.253L.447 1.42A1 1 0 0 0 0 2.253h1zm0 13H0a1 1 0 0 0 1.553.833L1 15.253zm8.447.833a1 1 0 1 0 1.107-1.666l-1.107 1.666zm0-14.666a1 1 0 1 0 1.107 1.666L9.447 1.42zM19 2.253h1a1 1 0 0 0-.447-.833L19 2.253zm0 13l-.553.833A1 1 0 0 0 20 15.253h-1zm-9.553-.833a1 1 0 1 0 1.107 1.666L9.447 14.42zM9 2.253v13h2v-13H9zm1.553-.833C9.203.523 7.42 0 5.5 0v2c1.572 0 2.961.431 3.947 1.086l1.107-1.666zM5.5 0C3.58 0 1.797.523.447 1.42l1.107 1.666C2.539 2.431 3.928 2 5.5 2V0zM0 2.253v13h2v-13H0zm1.553 13.833C2.539 15.431 3.928 15 5.5 15v-2c-1.92 0-3.703.523-5.053 1.42l1.107 1.666zM5.5 15c1.572 0 2.961.431 3.947 1.086l1.107-1.666C9.203 13.523 7.42 13 5.5 13v2zm5.053-11.914C11.539 2.431 12.928 2 14.5 2V0c-1.92 0-3.703.523-5.053 1.42l1.107 1.666zM14.5 2c1.573 0 2.961.431 3.947 1.086l1.107-1.666C18.203.523 16.421 0 14.5 0v2zm3.5.253v13h2v-13h-2zm1.553 12.167C18.203 13.523 16.421 13 14.5 13v2c1.573 0 2.961.431 3.947 1.086l1.107-1.666zM14.5 13c-1.92 0-3.703.523-5.053 1.42l1.107 1.666C11.539 15.431 12.928 15 14.5 15v-2z"
          />
        </svg>
      </div>
      <h1>Welcome to LibraryVue</h1>
      <SearchBox />
    </div>

    <div class="cards">
      <h2>Your Current Books</h2>
      <div class="card-grid issue-grid">
        <BookCard v-for="issue in issues" :key="issue.id" :book="issue.book" />
      </div>
    </div>

    <div class="cards">
      <h2>Books</h2>
      <div class="card-grid">
        <BookCard v-for="book in books" :key="book.id" :book="book" />
      </div>
    </div>

    <div class="cards">
      <h2>Sections</h2>
      <div class="card-grid">
        <SectionCard v-for="section in sections" :key="section.id" :section="section" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  display: grid;
  overflow: hidden;
  gap: 1rem;
}

.hero {
  display: grid;
  place-content: center;
  gap: 1rem;
  padding: 2rem;

  h1 {
    font-size: 5rem;
    font-weight: 700;
    text-align: center;
  }

  .app-logo {
    display: grid;
    place-content: center;
    color: var(--color-primary);
    svg {
      width: 100%;
      height: 100%;
    }
  }
}

.cards {
  max-width: 100%;
  display: grid;
  place-content: center;

  h2 {
    font-size: 2rem;
    font-weight: 700;
  }

  & .card-grid {
    display: grid;
    gap: 1rem;
    grid-auto-columns: 12rem;
    grid-auto-flow: column;
    overflow-x: auto;
    max-width: 80vw;
    padding: 1rem;
    border: 4px solid var(--color-secondary);
    border-radius: 0.5rem;
  }

  & .issue-grid {
    grid-auto-columns: 16rem;
    place-items: center;
  }
}
</style>
