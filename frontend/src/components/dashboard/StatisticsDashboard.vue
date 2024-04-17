<script setup lang="ts">
import LibrarianStatistics from '@/components/dashboard/LibrarianStatistics.vue'
import UserStatisitics from '@/components/dashboard/UserStatisitics.vue'

import { useStore } from '@/store'
import { computed } from 'vue'

const store = useStore()

const isUser = computed(() => store.getters.isUser)
const isLibrarian = computed(() => store.getters.isLibrarian)
</script>

<template>
  <UserStatisitics v-if="isUser" />
  <LibrarianStatistics v-if="isLibrarian" />
</template>
