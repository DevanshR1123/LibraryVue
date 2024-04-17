<script setup lang="ts">
import type { Book } from '@/types'
import { computed, ref } from 'vue'
import { useStore } from '@/store'

import UserComment from '@/components/comments/UserComment.vue'

const { book } = defineProps<{ book: Book }>()

const store = useStore()
const comment = ref('')

const isAuth = computed(() => store.getters.isAuth)
const isUser = computed(() => store.getters.isUser)

const canComment = computed(() => isAuth.value && isUser.value)

const createComment = () => {
  store.dispatch('createComment', { book_id: book.id, content: comment.value })
  comment.value = ''
}
</script>

<template>
  <div class="comments">
    <h2>Comments</h2>

    <div class="create-comment" v-if="canComment">
      <textarea v-model="comment" />
      <button @click="createComment" class="button create">Comment</button>
    </div>

    <ul v-if="book.comments.length" class="comments-list">
      <UserComment v-for="comment in book.comments" :key="comment.id" :comment="comment" />
    </ul>
    <p v-else>No comments yet</p>
  </div>
</template>

<style scoped>
.comments {
  grid-column: 1 / -1;
  display: grid;
  gap: 1rem;
}

.create-comment {
  display: grid;
  gap: 0.5rem;
  grid-template-columns: 1fr auto;
  grid-template-rows: 1fr auto;
}

textarea {
  width: 100%;
  min-height: 2lh;
  height: fit-content;
  resize: none;
  padding: 0.5rem;
  grid-column: 1 / -1;
}

.create {
  font-size: 1rem;
  grid-area: 2 / 2;
}

.comments-list {
  list-style: none;
  border: 1px solid var(--color-primary);
  border-radius: 0.5rem;
  display: grid;
  grid-template-columns: auto 1fr auto;
}
</style>
