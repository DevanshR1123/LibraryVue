<script setup lang="ts">
import BookCard from '@/components/books/BookCard.vue'
import { defineProps } from 'vue'
import { type Book, type Section } from '@/types'

const { books, sections } = defineProps({
  books: {
    type: Array as () => Book[],
    required: true
  },
  sections: {
    type: Array as () => Section[],
    required: true
  }
})

// console.log(books, sections)
</script>

<template>
  <section class="catalogue">
    <p v-if="!books.length" class="no-books">No books found</p>
    <BookCard v-for="book in books" :key="book.id" :book="book" />
  </section>
</template>

<style scoped>
.catalogue {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.no-books {
  text-align: center;
  color: var(--color-text-mute);
  grid-column: 1 / -1;
}
</style>
