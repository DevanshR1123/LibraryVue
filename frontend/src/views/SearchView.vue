<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useStore } from '@/store'
import { computed, ref } from 'vue'
import CrossIcon from '@/components/icons/CrossIcon.vue'
import BookCard from '@/components/books/BookCard.vue'
import SectionCard from '@/components/sections/SectionCard.vue'

const store = useStore()
const books = computed(() => store.state.books)
const sections = computed(() => store.state.sections)

const route = useRoute()

const searchQuery = (route.query.q as string) || ''
const search = ref(searchQuery)

const bookResults = computed(() => {
  if (search.value.trim() === '') return books.value

  return books.value.filter((book) =>
    `${book.title} ${book.author} ${book.year} ${book.description} ${book.section?.name}`
      .toLowerCase()
      .includes(search.value.toLowerCase())
  )
})

const sectionResults = computed(() => {
  if (search.value.trim() === '') return sections.value

  return sections.value.filter((section) =>
    `${section.name} ${section.description}`.toLowerCase().includes(search.value.toLowerCase())
  )
})

const clearSearch = () => {
  search.value = ''
}
</script>

<template>
  <div class="search">
    <form class="search-box">
      <input type="text" v-model="search" placeholder="Search catalogue..." />
      <button @click="clearSearch" class="cross" type="button">
        <CrossIcon />
      </button>
    </form>
    <section class="results">
      <h1 class="search-header" v-if="search">Search results for "{{ search }}"</h1>
      <h1 class="search-header" v-else>Sections</h1>
      <div class="catalogue">
        <p v-if="!sectionResults.length" class="no-books">No sections found</p>
        <SectionCard v-for="section in sectionResults" :key="section.id" :section="section" />
      </div>
    </section>
    <section class="results">
      <h1 class="search-header" v-if="search">Search results for "{{ search }}"</h1>
      <h1 class="search-header" v-else>Books</h1>
      <div class="catalogue">
        <p v-if="!bookResults.length" class="no-books">No books found</p>
        <BookCard v-for="book in bookResults" :key="book.id" :book="book" />
      </div>
    </section>
  </div>
</template>

<style scoped>
.search {
  display: grid;
  gap: 1rem;

  grid-template-rows: auto 1fr;
}

.results {
  display: grid;
  gap: 1rem;

  grid-template-rows: auto 1fr;
}

.catalogue {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(12rem, 1fr));
  gap: 2rem;

  grid-column: 1 / -1;

  align-self: start;
}

.search-header {
  font-size: 2.5rem;
}

.no-books {
  text-align: center;
  color: var(--color-text-mute);
  grid-column: 1 / -1;
}

.search-box {
  display: grid;
  align-items: center;
  /* justify-self: end; */
  gap: 0.5rem;

  padding: 1rem 8rem;
}

input {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: 1px solid var(--color-secondary);
  border-radius: 0.5rem;

  grid-area: 1 / 1;
}

.search-btn {
  padding: 0.5em 1em;
  border: none;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: bold;

  transition: all 200ms;
  cursor: pointer;

  font-size: 1rem;

  background-color: var(--color-primary);
  color: var(--color-background);
  border: 2px solid var(--color-primary);

  &:hover {
    color: var(--color-primary);
    background-color: var(--color-background);
  }
}

.cross {
  width: 1.25rem;
  aspect-ratio: 1 / 1;
  cursor: pointer;

  background-color: transparent;
  border: none;
  color: var(--text-light-2);

  grid-area: 1 / 1;

  justify-self: end;
  margin-right: 0.5rem;

  & svg {
    width: 100%;
    height: 100%;
  }
}
</style>
