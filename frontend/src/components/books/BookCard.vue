<script setup lang="ts">
import { computed } from 'vue'
import { type Book } from '@/types'
import BookPlaceholder from '@/components/BookPlaceholder.vue'

const props = defineProps({
  book: {
    type: Object as () => Book,
    required: true
  }
})

const { book } = props

const imgSrc = computed(() => `http://localhost:5000/images/${book.image}`)

const bookLink = computed(() => `/books/${book.id}`)
</script>

<template>
  <a class="book-card" :href="bookLink">
    <BookPlaceholder :src="imgSrc" />
    <div class="book-card-content">
      <h3 class="title">{{ book.title }}</h3>
      <p class="author">{{ book.author }}</p>
      <p class="year">{{ book.year }}</p>
    </div>
  </a>
</template>

<style scoped>
.book-card {
  border: 3px solid var(--color-secondary);
  background-color: var(--color-background-mute);
  border-radius: 0.5rem;

  color: var(--color-secondary);
  text-decoration: none;

  width: 100%;

  /* width: 16rem; */
  /* aspect-ratio: 3 / 4; */

  display: grid;
  gap: 0.5rem;
  grid-template-rows: 3fr 1fr;

  overflow: hidden;

  & img {
    width: 100%;
  }

  & .book-card-content {
    padding: 0 0.75rem 1rem;
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 0.25rem;
  }

  & p {
    font-size: 0.875rem;
    color: var(--color-text-mute);
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }

  & .title {
    font-size: 1.25rem;
    font-weight: bold;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;

    /* height: 2lh; */

    grid-column: 1 / -1;
  }

  & .author {
    font-size: 1rem;
  }

  & .year {
    font-size: 0.875rem;
    text-align: right;
  }
}
</style>
