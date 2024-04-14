<script setup lang="ts">
import { type LibrarianIssue } from '@/types'
import { useStore } from '@/store'

const { issues } = defineProps({
  issues: {
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
  <div class="active-issues">
    <h3>Active Issues</h3>
    <div class="issue-card" v-for="issue in issues" :key="issue.id">
      <div class="issue-info">
        <p v-if="include_title"><strong>Book:</strong> {{ issue.book.title }}</p>
        <p>
          <strong>Issued by:</strong> {{ issue.user.firstname }} {{ issue.user.lastname }} &#8212;
          {{ issue.user.email }}
        </p>
      </div>
      <div class="issue-actions">
        <button class="button delete" @click="store.dispatch('revokeBook', issue.id)">Revoke</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.active-issues {
  display: grid;
  gap: 1rem;
}

.issue-card {
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

  .issue-actions {
    display: flex;
    gap: 1rem;
  }
}
</style>
