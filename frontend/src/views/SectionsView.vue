<script setup lang="ts">
import { useStore } from '@/store'
import { computed } from 'vue'
import SectionCard from '@/components/books/SectionCard.vue'
import AdminToolbar from '@/components/AdminToolbar.vue'
import SearchBox from '@/components/SearchBox.vue'

const store = useStore()
const sections = computed(() => store.state.sections)
</script>

<template>
  <div class="sections">
    <h1>Sections</h1>
    <SearchBox />
    <AdminToolbar />

    <section class="section-cards">
      <p v-if="!sections.length" class="no-sections">No sections found</p>
      <SectionCard v-for="section in sections" :key="section.id" :section="section" />
    </section>
  </div>
</template>

<style scoped>
.sections {
  display: grid;
  gap: 1rem;
  grid-template-columns: 2fr 1fr;
}

h1 {
  margin-bottom: 1rem;
}

.toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
  gap: 1rem;
}

.section-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(14rem, 1fr));
  grid-auto-rows: 1fr;
  gap: 2rem;
  padding: 2rem;
  place-items: center;

  grid-column: 1 / -1;
}

.no-sections {
  text-align: center;
  color: var(--color-text-mute);
  grid-column: 1 / -1;
}
</style>
