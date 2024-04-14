<script setup lang="ts">
import { useStore } from '@/store'
import { computed } from 'vue'
import IssueRequests from '@/components/books/IssueRequests.vue'
import ActiveIssues from '@/components/books/ActiveIssues.vue'
import type { LibrarianIssue } from '@/types'

const store = useStore()

const requests = computed<LibrarianIssue[]>(() => store.getters.issue_requests)
const issues = computed<LibrarianIssue[]>(() => store.getters.active_issues)
</script>

<template>
  <div class="requests" v-if="requests.length">
    <IssueRequests :requests="requests" />
  </div>

  <div class="issues" v-if="issues.length">
    <ActiveIssues :issues="issues" />
  </div>
</template>

<style scoped>
.requests,
.issues {
  padding: 1rem;
}
</style>
