<script setup lang="ts">
import AddBookModal from '@/components/books/modals/AddBook.vue'
import { useStore } from '@/store'
import { computed } from 'vue'
import AddSectionModal from '@/components/sections/modals/AddSection.vue'

const store = useStore()
const isAdmin = computed(() => store.getters.isAdmin)
const isLibrarian = computed(() => store.getters.isLibrarian)
</script>

<template>
  <div class="toolbar" v-if="isAdmin || isLibrarian">
    <AddBookModal />
    <AddSectionModal />
  </div>
</template>

<style scoped>
.toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
  gap: 1rem;
  padding: 1rem;

  /* border: 2px solid var(--color-border); */
  border-radius: 0.5rem;
}
</style>
