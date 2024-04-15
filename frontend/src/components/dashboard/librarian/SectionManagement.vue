<script setup lang="ts">
import { useStore } from '@/store'
import { computed } from 'vue'
import EditSection from '@/components/sections/modals/EditSection.vue'
import DeleteSection from '@/components/sections/modals/DeleteSection.vue'
import SectionPlaceholder from '@/components/SectionPlaceholder.vue'

const store = useStore()

const sections = computed(() => store.getters.sections)

const isLibrarian = computed(() => store.getters.isLibrarian)
const isUser = computed(() => store.getters.isUser)
</script>

<template>
  <div class="section-management" v-if="isLibrarian">
    <h3>Section Management</h3>
    <div class="sections">
      <div class="section" v-for="section in sections" :key="section.id">
        <SectionPlaceholder :src="section.image ? `http://localhost:5000/images/${section.image}` : ''" />
        <div class="section-info">
          <p class="name"><strong>Name:</strong> {{ section.name }}</p>
          <p class="description"><strong>Description:</strong> {{ section.description }}</p>
          <p class="books"><strong>Books:</strong> {{ section.books.length }}</p>
        </div>
        <div class="section-actions">
          <EditSection :section="section" />
          <DeleteSection :section="section" />
        </div>
      </div>
    </div>
  </div>

  <div v-else class="unauthorized-view">
    <p>Only librarians can view this page.</p>
  </div>
</template>

<style scoped>
.section-management {
  display: grid;
  gap: 1rem;
}

.sections {
  display: grid;
  gap: 1rem;

  grid-auto-rows: 1fr;
}

img {
  border: 2px solid var(--color-secondary);
  border-radius: 0.5rem;
}

.section {
  display: grid;
  gap: 1rem;

  grid-template-columns: 8rem 1fr auto;
  align-items: center;

  background-color: var(--color-primary);

  padding: 1rem;
  border: 1px solid var(--color-secondary);
  border-radius: 0.5rem;
}

.section-info {
  display: grid;
  align-self: start;
}

.name {
  font-size: 1.5rem;
  border-bottom: 2px solid var(--color-secondary);
  margin-bottom: 0.5rem;
}

.section-actions {
  display: grid;
  gap: 1rem;
}
</style>
