<script setup lang="ts">
import BookCard from '@/components/books/BookCard.vue'
import { useStore } from '@/store'
import { computed } from 'vue'

const store = useStore()

const books = computed(() => store.state.books)
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
  grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.no-books {
  text-align: center;
  color: var(--color-text-mute);
  grid-column: 1 / -1;
}
</style>
