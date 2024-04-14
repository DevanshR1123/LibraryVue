<script setup lang="ts">
import { type LibrarianIssue } from '@/types'
import { useStore } from '@/store'

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
</script>

<template>
  <div class="issue-requests">
    <h3>Issue Requests</h3>
    <div class="request-card" v-for="request in requests" :key="request.id">
      <div class="request-info">
        <p v-if="include_title"><strong>Book:</strong> {{ request.book.title }}</p>
        <p>
          <strong>Requested by:</strong> {{ request.user.firstname }} {{ request.user.lastname }} &#8212;
          {{ request.user.email }}
        </p>
      </div>
      <div class="request-actions">
        <button class="button issue" @click="store.dispatch('grantBook', request.id)">Issue</button>
        <button class="button delete" @click="store.dispatch('rejectBook', request.id)">Reject</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
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
