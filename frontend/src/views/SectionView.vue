<script setup lang="ts">
import { useRoute, RouterLink } from 'vue-router'
import { ref } from 'vue'
import { type Section, type Book } from '@/types'
import SectionPlaceholder from '@/components/SectionPlaceholder.vue'
import BookCard from '@/components/books/BookCard.vue'

const route = useRoute()
const id = parseInt(route.params.id as string)

const error = ref<string | null>(null)
const name = ref<string | null>(null)
const description = ref<string | null>(null)
const imageUrl = ref<string | null>(null)
const books = ref<Book[]>([])

const res = await fetch(`http://localhost:5000/sections/${id}`)

if (res.ok) {
  const section: Section = await res.json()
  name.value = section.name
  description.value = section.description
  imageUrl.value = `http://localhost:5000/images/${section.image}`
  books.value = section.books || []
  route.meta.title = section.name
} else {
  const { message } = await res.json()
  error.value = message
}
</script>

<template>
  <section>
    <div class="section-card">
      <div class="section-img">
        <SectionPlaceholder :src="imageUrl" />
      </div>
      <h1 v-if="name">{{ name }}</h1>
      <p v-if="description">{{ description }}</p>
      <h1 v-if="error" class="error">{{ error }}</h1>
      <p v-if="error" class="error-link">
        <RouterLink to="/sections">Back to sections</RouterLink>
      </p>
    </div>
    <div class="catalogue">
      <p v-if="!books.length" class="no-books">No books found</p>
      <BookCard v-for="book in books" :key="book.id" :book="book" />
    </div>
  </section>
</template>

<style scoped>
.section-card {
  display: grid;
  grid-template-columns: 10rem 1fr;
  grid-template-rows: auto auto 1fr;
  gap: 0 2rem;

  .section-img {
    border-radius: 1rem;
    grid-column: 1;
    grid-row: span 3;
    border: 4px solid var(--color-primary);
    aspect-ratio: 1 / 1;
    display: grid;
    overflow: hidden;
  }

  h1 {
    font-size: 3rem;
    grid-column: 2;
    margin-top: 1rem;
  }

  p {
    grid-column: 2;
  }

  .error {
    color: var(--color-error);
    align-self: center;
    margin: 0;
  }

  .error-link {
    color: var(--color-secondary);
    font-weight: bold;

    a {
      color: var(--color-secondary);
    }
  }

  .error-link::before {
    content: '<< ';
    height: 1rem;
  }
}

.catalogue {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
  gap: 1rem;
  padding: 1rem;
}
</style>
