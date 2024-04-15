<script setup lang="ts">
import { useStore } from '@/store'
import { computed } from 'vue'
import { type LibrarianIssue } from '@/types'
import RevokeBook from '@/components/books/modals/RevokeBook.vue'
import ReturnBook from '@/components/books//modals/ReturnBook.vue'

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

const isLibrarian = computed(() => store.getters.isLibrarian)
const isUser = computed(() => store.getters.isUser)
</script>

<template>
  <div class="issues">
    <h3>Active Issues</h3>
    <div class="active-issues">
      <div class="issue-card" v-for="issue in issues" :key="issue.id">
        <div class="issue-info">
          <p v-if="include_title"><strong>Book:</strong> {{ issue.book.title }}</p>
          <p v-if="isLibrarian" class="user-info">
            <strong>Issued to:</strong> {{ issue.user.firstname }} {{ issue.user.lastname }} &#8212;
            {{ issue.user.email }}
          </p>
          <p class="issue-date">
            <strong>Issued on:</strong>
            {{ new Date(issue.issue_date).toLocaleDateString('en-IN', { dateStyle: 'full' }) }}
          </p>
          <p class="return-date">
            <strong>Return by:</strong>
            {{ new Date(issue.return_date).toLocaleDateString('en-IN', { dateStyle: 'full' }) }}
          </p>
          <p></p>
        </div>
        <div class="issue-actions">
          <RevokeBook :issue="issue" v-if="isLibrarian" />
          <RouterLink :to="`/read/${issue.book.id}`" class="button read" v-if="isUser"> Read </RouterLink>
          <ReturnBook :book="issue.book" v-if="isUser" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.issues {
  display: grid;
  gap: 1rem;
}

.active-issues {
  display: grid;
  gap: 1rem;
  grid-auto-rows: 1fr;
}

.issue-card {
  display: grid;
  gap: 1rem;

  grid-template-columns: 1fr auto;
  align-items: center;

  padding: 0.5rem;
  border-radius: 0.5rem;
  background-color: var(--color-primary-light);

  border: 2px solid var(--color-secondary);

  & .issue-info {
    display: grid;
    gap: 0.5rem 1rem;
    grid-template-columns: 2fr 1fr;
    place-content: start;

    & .issue-date {
      grid-column: 2;
      grid-row: 1;
    }

    & .return-date {
      grid-column: 2;
      grid-row: 2;
    }

    & .user-info {
      grid-column: 1;
    }
  }

  & .issue-actions {
    display: grid;
    gap: 0.5rem;
  }
}
</style>
