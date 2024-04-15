<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'
import { useStore } from '@/store'
import { computed } from 'vue'
import VuePdfEmbed from 'vue-pdf-embed'
import IssueBook from '@/components/books/modals/IssueBook.vue'

const route = useRoute()
const id = parseInt(route.params.id as string)

const store = useStore()
const isAuth = computed(() => store.getters.isAuth)
const isLibrarian = computed(() => store.getters.isLibrarian)
const isUser = computed(() => store.getters.isUser)

const book = computed(() => store.getters.book(id))
const title = computed(() => book.value?.title)

const content = computed(() => `http://localhost:5000/books/${id}/content`)

const issued = computed(() => store.getters.issued(id))
const canRead = computed(() => isAuth.value && ((isUser.value && issued.value) || isLibrarian.value))
const canIssue = computed(() => isAuth.value && isUser.value && !issued.value)
</script>

<template>
  <section class="reader">
    <div class="book-content" v-if="canRead">
      <h1>{{ title }}</h1>
      <VuePdfEmbed :source="content" />
    </div>

    <div v-else-if="canIssue && book" class="unauthorized-view">
      <h1>Book not issued</h1>
      <p>You need to issue this book to read it</p>
      <IssueBook :book="book" />
    </div>

    <div v-else-if="!book" class="unauthorized-view">
      <h1>Book not found</h1>
      <RouterLink to="/books" class="button">Back to Books</RouterLink>
    </div>

    <div v-else class="unauthorized-view">
      <h1>Unauthorized</h1>
      <p>You need to be logged in to read this book</p>
      <RouterLink to="/login" class="button">Login</RouterLink>
    </div>
  </section>
</template>

<style scoped>
.reader {
  display: grid;
  max-height: 100%;
  overflow: hidden;
}

.book-content {
  border: 4px solid var(--color-primary);
  border-radius: 0.25rem;
  display: grid;
  grid-template-columns: 5rem 1fr 5rem;
  padding-bottom: 1rem;
  gap: 1rem 0;

  overflow: hidden;

  h1 {
    text-align: center;
    background-color: var(--color-primary);
    color: var(--color-background);
    grid-column: span 3;
  }

  .vue-pdf-embed {
    grid-column: 2;
    display: grid;
    gap: 1rem;

    overflow: hidden auto;

    scrollbar-width: thin;
    scrollbar-color: var(--color-primary) var(--color-background-mute);

    .vue-pdf-embed__page {
      display: grid;
      place-items: center;
      border: 1px solid var(--color-border);
      border-radius: 0.25rem;

      & canvas {
        border-radius: inherit;
        max-width: 100%;
        max-height: 100%;
        overflow: hidden;
      }
    }

    &::-webkit-scrollbar {
      width: 0.5rem;
    }

    &::-webkit-scrollbar-thumb {
      background-color: var(--color-primary);
      border-radius: 0.25rem;
    }

    &::-webkit-scrollbar-track {
      background-color: var(--color-background-mute);
    }

    &::-webkit-scrollbar-corner {
      background-color: var(--color-background);
    }

    &::-webkit-scrollbar-thumb:hover {
      background-color: var(--color-primary-dark);
    }
  }
}

.unauthorized-view {
  display: grid;
  gap: 1rem;
  place-content: center;
  text-align: center;
  font-size: 1.5rem;

  h1 {
    font-size: 2.5rem;
  }

  p {
    font-size: 1.5rem;
  }

  .button {
    padding: 0.5rem 1rem;
    border: 2px solid var(--color-primary);
    border-radius: 0.5rem;
    background-color: var(--color-primary);
    color: var(--color-background);
    font-weight: bold;

    font-size: 1.25rem;

    place-self: center;

    transition:
      background-color 500ms,
      color 500ms;

    &:hover {
      background-color: var(--color-background);
      color: var(--color-primary);
    }
  }
}

a {
  color: var(--color-text);
  text-decoration: none;
  font-weight: bold;
}
</style>
