<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const id = route.params.id
</script>

<template>
  <section class="book">
    <h1>Book {{ id }}</h1>
  </section>
</template>

<style scoped></style>
