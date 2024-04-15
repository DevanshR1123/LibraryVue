<script setup lang="ts">
import { useStore } from '@/store'
import { computed } from 'vue'
import { type LibrarianIssue } from '@/types'
import GrantBook from '@/components/books/modals/GrantBook.vue'
import RejectBook from '@/components/books/modals/RejectBook.vue'
import UnissueBook from './modals/UnissueBook.vue'

const { requests } = defineProps({
  requests: {
    type: Array as () => LibrarianIssue[],
    required: true
  },

  include_title: {
    type: Boolean,
    default: true
  }
})

const store = useStore()

const isLibrarian = computed(() => store.getters.isLibrarian)
const isUser = computed(() => store.getters.isUser)
</script>

<template>
  <div class="requests">
    <h3>Issue Requests</h3>
    <div class="issue-requests">
      <div class="request-card" v-for="request in requests" :key="request.id">
        <div class="request-info">
          <p v-if="include_title"><strong>Book:</strong> {{ request.book.title }}</p>
          <p v-if="!isUser">
            <strong>Requested by:</strong> {{ request.user.firstname }} {{ request.user.lastname }} &#8212;
            {{ request.user.email }}
          </p>
        </div>
        <div class="request-actions">
          <GrantBook :issue="request" v-if="isLibrarian" />
          <RejectBook :issue="request" v-if="isLibrarian" />
          <UnissueBook :book="request.book" v-if="isUser" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.requests {
  display: grid;
  gap: 1rem;
}

.issue-requests {
  display: grid;
  gap: 1rem;
}

.request-card {
  display: grid;
  gap: 1rem;

  grid-template-columns: 1fr auto;
  align-items: center;

  padding: 0.5rem;
  border-radius: 0.5rem;
  background-color: var(--color-primary-light);

  border: 2px solid var(--color-secondary);

  .request-info {
    display: grid;
    gap: 0.5rem;
  }

  .request-actions {
    display: grid;
    gap: 0.5rem;
  }
}
</style>
