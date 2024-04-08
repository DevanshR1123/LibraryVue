<script setup lang="ts">
import CatalogueSection from '@/components/books/CatalogueSection.vue'
import AddBookModal from '@/components/books/AddBookModal.vue'
import { useStore } from '@/store'
import { computed } from 'vue'

const store = useStore()
const isAdmin = computed(() => store.getters.isAdmin)
const isLibrarian = computed(() => store.getters.isLibrarian)
</script>

<template>
  <div class="books">
    <h1>Books</h1>

    <div class="toolbar" v-if="isAdmin || isLibrarian">
      <AddBookModal />
    </div>

    <Suspense>
      <CatalogueSection />
      <template #fallback>
        <div class="loader"></div>
      </template>
    </Suspense>
  </div>
</template>

<style scoped>
h1 {
  margin-bottom: 1rem;
}
</style>
