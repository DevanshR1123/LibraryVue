<script setup lang="ts">
import { computed } from 'vue'
import { type Section } from '@/types'
import SectionPlaceholder from '@/components/SectionPlaceholder.vue'

const props = defineProps({
  section: {
    type: Object as () => Section,
    required: true
  }
})

const { section } = props

const imgSrc = computed(() =>
  section.image ? `http://localhost:5000/images/${section.image}` : null
)
const sectionLink = computed(() => `/sections/${section.id}`)
</script>

<template>
  <a :href="sectionLink" class="section-card">
    <SectionPlaceholder :src="imgSrc" />
    <div class="section-card-content">
      <h3 class="name">{{ section.name }}</h3>
      <p class="description">
        {{ section.description }}
      </p>
    </div>
  </a>
</template>

<style scoped>
.section-card {
  border: 3px solid var(--color-secondary);
  background-color: var(--color-background-mute);
  border-radius: 0.5rem;

  color: var(--color-secondary);
  text-decoration: none;

  width: 100%;

  display: grid;
  gap: 0.5rem;

  overflow: hidden;

  & img {
    width: 100%;
  }

  & .section-card-content {
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

  & .name {
    font-size: 1.25rem;
    font-weight: bold;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;

    grid-column: 1 / -1;
  }

  & .description {
    font-size: 1rem;
  }
}
</style>
