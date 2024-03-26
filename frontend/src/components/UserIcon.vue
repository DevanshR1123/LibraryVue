<script setup lang="ts"></script>

<template>
  <div class="icon">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
      <path
        d="M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H418.3c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304H178.3z"
      />
    </svg>
  </div>
</template>

<style scoped>
.icon {
  --size: 2.5rem;

  width: var(--size);
  aspect-ratio: 1;

  display: grid;
  place-items: center;
  place-self: center;

  background-color: var(--color-primary);
  color: var(--color-background);

  border-radius: 50%;
  padding: calc(var(--size) / 4);

  border: 2px solid var(--color-secondary);

  svg {
    width: 100%;
    height: 100%;
  }
}
</style>
