<script setup lang="ts">
import { computed } from 'vue'
import { useStore } from '@/store'

const store = useStore()

const user = computed(() => store.state.user)

const books = computed(() => store.getters.books)
const sections = computed(() => store.getters.sections)
</script>

<template>
  <div class="librarian-dashboard">
    <div class="summary-statistics">
      <div class="statistic">
        <h3>{{ books.length }}</h3>
        <p>Books</p>
      </div>
      <div class="statistic">
        <h3>{{ sections.length }}</h3>
        <p>Sections</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.summary-statistics {
  display: grid;
  border: 4px solid var(--color-secondary);
  border-radius: 1rem;
  padding: 1rem;

  & .statistic {
    display: flex;
    gap: 0.5rem;
    align-items: center;
  }

  & h3 {
    font-size: 1.5rem;
  }
}
</style>
