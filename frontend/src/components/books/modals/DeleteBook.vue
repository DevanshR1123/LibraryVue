<script setup lang="ts">
import { ref } from 'vue'
import { useStore } from '@/store'
import { toast } from 'vue3-toastify'
import { useRouter } from 'vue-router'
import { type Book } from '@/types'

const router = useRouter()

const { book } = defineProps<{ book: Book }>()

const store = useStore()

const dialog = ref<HTMLDialogElement>()

const showModal = () => {
  dialog.value!.showModal()
}

const closeModal = () => {
  dialog.value!.close()
}

const deleteBook = async () => {
  try {
    await store.dispatch('deleteBook', book.id)
    if (router.currentRoute.value.name === 'book') router.push('/books')
  } catch (error) {
    console.error(error)
    toast.error('Failed to delete book')
  }

  closeModal()
}
</script>

<template>
  <dialog ref="dialog" class="book-modal">
    <h2>Delete Book</h2>
    <form @submit.prevent="deleteBook">
      <p>
        Are you sure you want to delete <strong>"{{ book.title }}"</strong> by <strong>{{ book.author }}</strong
        >?
      </p>

      <div class="btns">
        <button type="submit" class="button delete">Delete</button>
        <button type="button" class="button issue" @click="closeModal">Cancel</button>
      </div>
    </form>
  </dialog>

  <button class="button delete" @click="showModal">Delete Book</button>
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
