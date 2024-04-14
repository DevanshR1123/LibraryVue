<script setup lang="ts">
import AdminToolbar from '@/components/AdminToolbar.vue'
import SearchBox from '@/components/SearchBox.vue'
import BookCard from '@/components/books/BookCard.vue'
import { useStore } from '@/store'
import { computed } from 'vue'

const store = useStore()
const books = computed(() => store.state.books)
</script>

<template>
  <div class="books">
    <h1>Books</h1>
    <SearchBox />
    <AdminToolbar />

    <section class="book-cards">
      <p v-if="!books.length" class="no-books">No books found</p>
      <BookCard v-for="book in books" :key="book.id" :book="book" />
    </section>
  </div>
</template>

<style scoped>
.books {
  display: grid;
  gap: 1rem;

  grid-template-columns: 2fr 1fr;
  grid-template-rows: auto auto 1fr;
}

.toolbar {
  grid-column: 1 / -1;
}

.book-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(14rem, 1fr));
  gap: 2rem;
  padding: 2rem;
  place-items: center;
  align-self: start;

  grid-column: 1 / -1;
}

.no-books {
  text-align: center;
  color: var(--color-text-mute);
  grid-column: 1 / -1;
}
</style>
