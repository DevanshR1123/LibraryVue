<script setup lang="ts">
import { useStore } from '@/store'
import { computed } from 'vue'
import SectionCard from '@/components/sections/SectionCard.vue'
import AdminToolbar from '@/components/AdminToolbar.vue'
import SearchBox from '@/components/SearchBox.vue'

const store = useStore()
const sections = computed(() => store.state.sections)
</script>

<template>
  <div class="sections">
    <h1>Library Sections</h1>
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
  grid-template-rows: auto 1fr;
}

.toolbar {
  grid-column: 1 / -1;
}

.section-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(14rem, 1fr));
  grid-auto-rows: 1fr;
  gap: 2rem;
  padding: 2rem;
  place-items: center;
  align-self: start;

  grid-column: 1 / -1;
}

.no-sections {
  text-align: center;
  color: var(--color-text-mute);
  grid-column: 1 / -1;
}
</style>
