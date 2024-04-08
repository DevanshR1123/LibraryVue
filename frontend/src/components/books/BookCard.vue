<script setup lang="ts">
import { defineProps } from 'vue'
import { type Book } from '@/types'

const props = defineProps({
  book: {
    type: Object as () => Book,
    required: true
  }
})

const { book } = props
</script>

<template>
  <div class="book-card">
    <h2>{{ book.title }}</h2>
    <p>{{ book.author }}</p>
    <p>{{ book.year }}</p>
  </div>
</template>

<style scoped>
.book-card {
  border: 1px solid var(--color-border);
  padding: 1rem;
  margin: 1rem;
  border-radius: 0.5rem;
}
</style>
