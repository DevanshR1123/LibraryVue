<script setup lang="ts">
import { ref, defineProps, onMounted, reactive } from 'vue'
import { type Section } from '@/types'
import {} from '@/utils/api'
import BookPlaceholder from '@/components/BookPlaceholder.vue'
</script>

<template>
  <dialog ref="dialog" class="add-section-modal">
    <h2>Add Section</h2>
    <form @submit.prevent="addSection">
      <label for="name">Name</label>
      <input type="text" id="name" v-model="section.name" required />
      <button type="submit">Add</button>
    </form>
  </dialog>

  <button @click="openModal">Add Section</button>
</template>
