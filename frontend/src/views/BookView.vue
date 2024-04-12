<script setup lang="ts">
import { useRoute } from 'vue-router'
import { ref } from 'vue'
import { type Book } from '@/types'
import BookPlaceholder from '@/components/BookPlaceholder.vue'

const route = useRoute()
const id = parseInt(route.params.id as string)

const error = ref<string | null>(null)
const title = ref<string | null>(null)
const description = ref<string | null>(null)
const imageUrl = ref<string | null>(null)
const author = ref<string | null>(null)
const isbn = ref<string | null>(null)
const year = ref<number | null>(null)
const content = ref<string | null>(null)

const res = await fetch(`http://localhost:5000/books/${id}`)

if (res.ok) {
  const book: Book = await res.json()
  title.value = book.title
  description.value = book.description
  imageUrl.value = `http://localhost:5000/images/${book.image}`
  author.value = book.author
  isbn.value = book.isbn
  year.value = book.year
  content.value = book.content as string

  route.meta.title = book.title
} else {
  const { message } = await res.json()
  error.value = message
}
</script>

<template>
  <section class="book">
    <div class="book-card">
      <div class="book-img">
        <BookPlaceholder :src="imageUrl" />
      </div>
      <h1 v-if="title">{{ title }}</h1>
      <p v-if="description">{{ description }}</p>
      <div class="book-info">
        <p v-if="author"><strong>Author:</strong> {{ author }}</p>
        <p v-if="year"><strong>Year:</strong> {{ year }}</p>
        <p v-if="isbn"><strong>ISBN:</strong> {{ isbn }}</p>
        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="error" class="error-link">
          <RouterLink to="/books">Back to books</RouterLink>
        </p>
      </div>
    </div>
    <!-- <div class="book-content" v-if="content" v-html="content"></div>  -->
  </section>
</template>

<style scoped>
.book {
  display: grid;
  gap: 2rem;

  grid-template-rows: auto 1fr;
}

.book-card {
  display: grid;
  grid-template-columns: 10rem 1fr;
  grid-template-rows: auto auto 1fr;
  gap: 0 2rem;

  .book-img {
    border-radius: 1rem;
    grid-column: 1;
    grid-row: span 3;
    border: 4px solid var(--color-primary);
    aspect-ratio: 1 / 1;
    display: grid;
    overflow: hidden;
  }

  .book-info {
    grid-column: 2;

    display: flex;
    gap: 1rem;
  }
}

.book-content {
  font-size: 1.125rem;
  line-height: 1.75;
}

.error {
  color: var(--color-error);
  margin: 0;
}

.error-link {
  margin: 0;
}
</style>
