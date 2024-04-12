<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import CrossIcon from '@/components/icons/CrossIcon.vue'

const search = ref('')
const router = useRouter()

const searchHandler = () => {
  if (search.value.trim() !== '') {
    router.push(`/search?q=${search.value}`)
  }
}

const clearSearch = () => {
  search.value = ''
}
</script>

<template>
  <form class="search-box" @submit.prevent="searchHandler">
    <input type="text" v-model="search" placeholder="Search catalogue..." />
    <button type="submit" class="search-btn">Search</button>
    <button @click="clearSearch" class="cross">
      <CrossIcon />
    </button>
  </form>
</template>

<style scoped>
.search-box {
  display: grid;
  align-items: center;
  /* justify-self: end; */
  gap: 0.5rem;

  grid-template-columns: 1fr auto;
}

input {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: 1px solid var(--color-secondary);
  border-radius: 0.5rem;

  grid-area: 1 / 1;
}

.search-btn {
  padding: 0.5em 1em;
  border: none;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: bold;

  transition: all 200ms;
  cursor: pointer;

  font-size: 1rem;

  background-color: var(--color-primary);
  color: var(--color-background);
  border: 2px solid var(--color-primary);

  &:hover {
    color: var(--color-primary);
    background-color: var(--color-background);
  }
}

.cross {
  width: 1.25rem;
  aspect-ratio: 1 / 1;
  cursor: pointer;

  background-color: transparent;
  border: none;
  color: var(--text-light-2);

  grid-area: 1 / 1;

  justify-self: end;
  margin-right: 0.5rem;

  & svg {
    width: 100%;
    height: 100%;
  }
}
</style>
