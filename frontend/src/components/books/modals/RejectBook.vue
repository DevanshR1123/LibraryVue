<script setup lang="ts">
import { ref } from 'vue'
import { useStore } from '@/store'
import { toast } from 'vue3-toastify'
import type { LibrarianIssue } from '@/types'

const { issue } = defineProps<{ issue: LibrarianIssue }>()

const store = useStore()

const dialog = ref<HTMLDialogElement>()

const showModal = () => {
  dialog.value!.showModal()
}

const closeModal = () => {
  dialog.value!.close()
}

const rejectBook = async () => {
  try {
    await store.dispatch('rejectBook', issue.id)
  } catch (error) {
    console.error(error)
    toast.error('Failed to issue book')
  }

  closeModal()
}
</script>

<template>
  <dialog ref="dialog" class="book-modal">
    <h2>Grant Issue</h2>
    <form @submit.prevent="rejectBook">
      <p>
        Are you sure you want to reject the book <strong>{{ issue.book.title }}</strong> requested by
        <strong>{{ issue.user.firstname }} {{ issue.user.lastname }}</strong> ?
      </p>

      <div class="btns">
        <button type="button" class="button issue" @click="closeModal">Cancel</button>
        <button type="submit" class="button cancel">Reject Issue</button>
      </div>
    </form>
  </dialog>

  <button class="button cancel" @click="showModal">Reject</button>
</template>

<style scoped>
.book-modal {
  padding: 2rem;
  max-width: 32rem;

  & form {
    display: grid;
    gap: 1rem;
    text-align: center;
    text-wrap: balance;
  }
}

h2 {
  text-align: center;
  margin-bottom: 1rem;
  font-size: 2rem;
  grid-column: 1 / -1;
}

.btns {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(2, 1fr);
  grid-column: 1 / -1;
  margin-top: 1rem;
}
</style>
