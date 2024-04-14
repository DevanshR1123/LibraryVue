<script setup lang="ts">
import { useRoute, RouterLink } from 'vue-router'
import { ref, computed } from 'vue'
import { type Section, type Book } from '@/types'
import SectionPlaceholder from '@/components/SectionPlaceholder.vue'
import BookCard from '@/components/books/BookCard.vue'
import DeleteSection from '@/components/sections/modals/DeleteSection.vue'
import EditSection from '@/components/sections/modals/EditSection.vue'

import { useStore } from '@/store'

const store = useStore()

const route = useRoute()
const id = parseInt(route.params.id as string)

const isLibrarian = computed(() => store.getters.isLibrarian)
const isAdmin = computed(() => store.getters.isAdmin)

const section = computed<Section>(() => store.getters.section(id))
const error = computed(() => !section.value && 'Section not found')

const name = computed(() => section.value?.name)
const description = computed(() => section.value?.description)
const imageUrl = computed(() =>
  section.value?.image ? `http://localhost:5000/images/${section.value?.image}` : undefined
)
const books = computed<Book[]>(() => section.value?.books || [])

const canModify = computed(() => isAdmin.value || isLibrarian.value)
</script>

<template>
  <div class="section-view">
    <section class="section">
      <div class="section-card">
        <div class="section-img">
          <SectionPlaceholder :src="imageUrl" />
        </div>
        <template v-if="error">
          <h1 class="error">{{ error }}</h1>
          <p class="error-message">
            The section you are looking for does not exist. Please check back later.
          </p>
        </template>
        <template v-else>
          <h1 class="section-title">{{ name }}</h1>
          <p class="section-description">{{ description }}</p>

          <div class="section-actions">
            <EditSection :section="section" v-if="canModify" />
            <DeleteSection :section="section" v-if="canModify" />
          </div>

          <div class="catalogue">
            <p v-if="!books.length" class="no-books">No books found</p>
            <BookCard v-for="book in books" :key="book.id" :book="book" />
          </div>
        </template>
      </div>
    </section>
  </div>
</template>

<style scoped>
.section-card {
  display: grid;
  grid-template-columns: 10rem 1fr auto;
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
}

.catalogue {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
  gap: 1rem;
  padding: 1rem;

  grid-column: 1 / -1;
}

.section-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;

  padding: 1rem 0;
  border-radius: 0.5rem;
  margin: 1rem 0;

  grid-column: 3 / -1;
  grid-row: 1 / span 3;
}
</style>
