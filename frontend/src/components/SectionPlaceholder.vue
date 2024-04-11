<script setup lang="ts">
const { src } = defineProps({
  src: {
    type: String as () => string | null,
    default: ''
  }
})
</script>

<template>
  <img :src="src" alt="Section cover" v-if="src" />
  <div class="alt-img" v-else>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" fill="currentColor">
      <path
        d="M96 0C43 0 0 43 0 96V416c0 53 43 96 96 96H384h32c17.7 0 32-14.3 32-32s-14.3-32-32-32V384c17.7 0 32-14.3 32-32V32c0-17.7-14.3-32-32-32H384 96zm0 384H352v64H96c-17.7 0-32-14.3-32-32s14.3-32 32-32zm32-240c0-8.8 7.2-16 16-16H336c8.8 0 16 7.2 16 16s-7.2 16-16 16H144c-8.8 0-16-7.2-16-16zm16 48H336c8.8 0 16 7.2 16 16s-7.2 16-16 16H144c-8.8 0-16-7.2-16-16s7.2-16 16-16z"
      />
    </svg>
  </div>
</template>

<style scoped>
img {
  width: 100%;
  object-fit: contain;
}

.alt-img {
  display: grid;
  place-items: center;
  background-color: var(--color-primary-light);
  color: var(--indigo);
  font-size: 1.5rem;
  padding: 3rem;
  aspect-ratio: 1 / 1;
}

svg {
  width: 100%;
  height: 100%;
}
</style>
