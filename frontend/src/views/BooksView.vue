<script setup lang="ts">
import CatalogueSection from '@/components/books/CatalogueSection.vue'
import AddBookModal from '@/components/books/AddBookModal.vue'
import { useStore } from '@/store'
import { computed } from 'vue'
import { getSections, getBooks } from '@/utils/api'
import { useRouter } from 'vue-router'

const store = useStore()

const isAuth = computed(() => store.getters.isAuth)
const router = useRouter()

if (!isAuth.value) router.push('/login')

const isAdmin = computed(() => store.getters.isAdmin)
const isLibrarian = computed(() => store.getters.isLibrarian)

const sections = await getSections()
const books = await getBooks()
</script>

<template>
  <div class="books">
    <h1>Books</h1>

    <div class="toolbar" v-if="isAdmin || isLibrarian">
      <AddBookModal :sections="sections" />
    </div>

    <CatalogueSection :sections="sections" :books="books" />
  </div>
</template>

<style scoped>
h1 {
  margin-bottom: 1rem;
}

.toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}
</style>
