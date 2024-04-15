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
  <div class="issue-management">
    <IssueRequests :requests="requests" v-if="requests.length" />
    <ActiveIssues :issues="issues" v-if="issues.length" />
  </div>
</template>

<style scoped>
.issue-management {
  display: grid;
  gap: 2rem;
}
</style>
