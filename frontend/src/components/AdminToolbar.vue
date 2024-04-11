<script setup lang="ts">
import AddBookModal from '@/components/books/AddBookModal.vue'
import { useStore } from '@/store'
import { computed } from 'vue'
import AddSectionModal from '@/components/books/AddSectionModal.vue'

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
}
</style>
