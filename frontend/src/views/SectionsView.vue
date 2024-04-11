<script setup lang="ts">
import { useStore } from '@/store'
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import SectionCard from '@/components/books/SectionCard.vue'
import AdminToolbar from '@/components/AdminToolbar.vue'

const store = useStore()

const isAuth = computed(() => store.getters.isAuth)
const router = useRouter()

if (!isAuth.value) router.push('/login')

const sections = computed(() => store.state.sections)
</script>

<template>
  <div class="sections">
    <h1>Sections</h1>

    <AdminToolbar />

    <section class="section-cards">
      <SectionCard v-for="section in sections" :key="section.id" :section="section" />
    </section>
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
  gap: 1rem;
}

.section-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(14rem, 1fr));
  grid-auto-rows: 1fr;
  gap: 1rem;
  padding: 2rem;
  place-items: center;
}
</style>
