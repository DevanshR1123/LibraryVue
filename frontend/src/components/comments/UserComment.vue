<script setup lang="ts">
import type { Comment } from '@/types'
import { computed } from 'vue'
import { useStore } from '@/store'

const { comment } = defineProps<{ comment: Comment }>()

const store = useStore()
const isAuth = computed(() => store.getters.isAuth)
const isUser = computed(() => store.getters.isUser)
const isLibrarian = computed(() => store.getters.isLibrarian)

const byUser = computed(() => store.getters.comment_by_user(comment.id))
// const comments = computed(() => store.getters.comments)

const canDelete = computed(() => isAuth.value && ((isUser.value && byUser.value) || isLibrarian.value))
</script>

<template>
  <li class="comment">
    <strong class="username">{{ comment.username }}:</strong>
    <div class="comment-content">
      <p class="content">
        {{ comment.content }}
      </p>
      <small class="timestamp">
        {{ new Date(comment.timestamp).toLocaleString('en-IN', { dateStyle: 'long', timeStyle: 'short' }) }}
      </small>
    </div>

    <div class="comment-actions">
      <button v-if="canDelete" @click="store.dispatch('deleteComment', comment.id)" class="button delete">
        Delete
      </button>
    </div>
  </li>
</template>

<style scoped>
.comment {
  padding: 0.5rem;
  border-bottom: 1px solid var(--color-primary);

  display: grid;
  gap: 0.5rem;
  grid-template-columns: subgrid;
  grid-template-rows: 1fr auto;
  grid-column: 1 / -1;

  .username {
    font-size: 1rem;
  }

  &:last-child {
    border-bottom: none;
  }

  &:nth-child(even) {
    background-color: var(--color-primary-light);
  }

  .comment-content {
    display: grid;
    gap: 0.5rem;
    grid-template-rows: subgrid;
    grid-row: 1 / -1;
    grid-column: 2;
  }

  .content {
    font-size: 1rem;
  }

  .timestamp {
    font-size: 0.8rem;
    color: var(--text-light-2);
  }

  .comment-actions {
    display: grid;
    gap: 0.5rem;
    grid-column: 3;
    grid-row: 1 / -1;

    place-items: start end;

    .delete {
      font-size: 1rem;
    }
  }
}
</style>
