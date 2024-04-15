<script setup lang="ts">
import { useStore } from '@/store'
import { computed } from 'vue'
import DeleteBook from '@/components/books/modals/DeleteBook.vue'
import EditBook from '@/components/books/modals/EditBook.vue'
import BookPlaceholder from '@/components/BookPlaceholder.vue'
import BookCard from '@/components/books/BookCard.vue'

const store = useStore()

const books = computed(() => store.getters.books)
const isLibrarian = computed(() => store.getters.isLibrarian)
const isUser = computed(() => store.getters.isUser)
const issues = computed(() => store.getters.active_issues)
</script>

<template>
  <div class="books-management" v-if="isLibrarian">
    <div class="books">
      <div class="book" v-for="book in books" :key="book.id">
        <BookPlaceholder :src="book.image ? `http://localhost:5000/images/${book.image}` : ''" />
        <div class="book-info">
          <p class="title">{{ book.title }}</p>
          <p class="author"><strong>Author:</strong> {{ book.author }}</p>
          <p class="year"><strong>Section:</strong> {{ book.section.name }}</p>
          <p class="isbn"><strong>ISBN:</strong> {{ book.isbn }}</p>
          <div class="description"><strong>Description:</strong> {{ book.description }}</div>
        </div>
        <div class="book-actions">
          <EditBook :book="book" />
          <DeleteBook :book="book" />
          <RouterLink :to="`/read/${book.id}`" class="button read">Read Book</RouterLink>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="isUser" class="my-books">
    <!-- <div class="books">
      <div class="book" v-for="issue in issues" :key="issue.id">
        <BookPlaceholder :src="issue.book.image ? `http://localhost:5000/images/${issue.book.image}` : ''" />
        <div class="book-info">
          <p class="title">{{ issue.book.title }}</p>
          <p class="author"><strong>Author:</strong> {{ issue.book.author }}</p>
          <p class="year"><strong>Section:</strong> {{ issue.book.section.name }}</p>
          <p class="isbn"><strong>ISBN:</strong> {{ issue.book.isbn }}</p>
          <div class="description"><strong>Description:</strong> {{ issue.book.description }}</div>
        </div>
        <div class="book-actions">
          <RouterLink :to="`/read/${issue.book.id}`" class="button read">Read Book</RouterLink>
          <ReturnBook :book="issue.book" />
        </div>
      </div>
    </div> -->

    <BookCard v-for="issue in issues" :key="issue.id" :book="issue.book" />
  </div>

  <div v-else class="unauthorized-view">
    <p>Only librarians can access this page.</p>
  </div>
</template>

<style scoped>
.books-management {
  display: grid;
  gap: 1rem;
}

img {
  border: 2px solid var(--color-secondary);
  border-radius: 0.5rem;
}

.books {
  display: grid;
  gap: 1rem;

  grid-auto-rows: 1fr;
}

.my-books {
  display: grid;
  gap: 1rem;

  grid-auto-rows: 1fr;
  grid-template-columns: repeat(auto-fill, minmax(20rem, 1fr));
}

.book {
  display: grid;
  gap: 1rem;

  grid-template-columns: 12rem 1fr auto;
  align-items: center;

  padding: 1rem;
  border-radius: 1rem;
  background-color: var(--color-primary-light);
  border: 1px solid var(--color-secondary);
}

.book-info {
  display: grid;
  gap: 0.5rem 2rem;
  align-self: start;

  grid-template-columns: auto 1fr;
}

.title {
  grid-column: 1 / span 2;
  font-size: 1.5rem;
  border-bottom: 2px solid var(--color-secondary);
  margin-bottom: 0.5rem;
}

.description {
  grid-column: 2;
  grid-row: 2 / span 3;

  text-wrap: balance;
}

.book-actions {
  display: grid;
  gap: 0.5rem;
  align-items: center;
}
</style>
