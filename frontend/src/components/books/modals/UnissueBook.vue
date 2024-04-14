<script setup lang="ts">
import { ref } from 'vue'
import { useStore } from '@/store'
import { toast } from 'vue3-toastify'
import { type Book } from '@/types'

const { book } = defineProps<{ book: Book }>()

const store = useStore()

const dialog = ref<HTMLDialogElement>()

const showModal = () => {
  dialog.value!.showModal()
}

const closeModal = () => {
  dialog.value!.close()
}

const unissueBook = async () => {
  try {
    await store.dispatch('unissueBook', book.id)
  } catch (error) {
    console.error(error)
    toast.error('Failed to delete book')
  }

  closeModal()
}
</script>

<template>
  <dialog ref="dialog" class="unissue-book-modal">
    <h2>Delete Book</h2>
    <form @submit.prevent="unissueBook">
      <p>
        Are you sure you want to cancel issue request for <strong>"{{ book.title }}"</strong> by
        <strong>{{ book.author }}</strong> ?
      </p>

      <div class="btns">
        <button type="submit" class="button unissue">Unissue Book</button>
        <button type="button" class="button issue" @click="closeModal">Cancel Unissue</button>
      </div>
    </form>
  </dialog>

  <button class="button unissue" @click="showModal">Unissue Book</button>
</template>

<style scoped>
.unissue-book-modal {
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
