<script setup lang="ts">
import { ref, defineProps } from 'vue'
import { type Section } from '@/types'
// import { addBook } from '@/utils/api'

const { sections } = defineProps({
  sections: {
    type: Array as () => Section[],
    required: true
  }
})

const title = ref()
const author = ref()
const description = ref()
const isbn = ref()
const year = ref()
const content = ref<HTMLInputElement>()
const image = ref<HTMLInputElement>()

const addBook = async () => {
  console.log(
    title.value,
    author.value,
    description.value,
    isbn.value,
    year.value,
    content.value,
    image.value
  )
}

const dialog = ref<HTMLDialogElement>()

const showModal = () => {
  dialog.value!.showModal()
}

const hideModal = () => {
  dialog.value!.close()
}
</script>

<template>
  <dialog ref="dialog" class="add-book-modal">
    <form @submit.prevent="addBook">
      <label for="title"
        >Title
        <input type="text" id="title" name="title" required v-model="title" />
      </label>

      <label for="author"
        >Author
        <input type="text" id="author" name="author" required v-model="author" />
      </label>

      <label for="description"
        >Description
        <textarea id="description" name="description" required v-model="description"></textarea>
      </label>

      <label for="isbn"
        >ISBN
        <input type="text" id="isbn" name="isbn" required v-model="isbn" />
      </label>

      <label for="year"
        >Year
        <input type="number" id="year" name="year" required v-model="year" />
      </label>

      <label for="content"
        >Content
        <input
          type="file"
          id="content"
          name="content"
          required
          ref="content"
          accept="application/pdf"
        />
      </label>

      <label for="image"
        >Image
        <input type="file" id="image" name="image" required ref="image" accept="image/*" />
      </label>

      <div class="btns">
        <button type="submit">Add</button>
        <button type="button" @click="hideModal">Cancel</button>
      </div>
    </form>
  </dialog>

  <button @click="showModal">Add Book</button>
</template>

<style scoped>
.add-book-modal {
  padding: 2rem;

  & form {
    display: grid;
    gap: 1rem;
  }

  & label {
    display: grid;
    gap: 0.25em;
    font-size: 0.875rem;
  }

  & input {
    padding: 0.5rem;
    font-size: 1rem;
  }
}

button {
  padding: 0.5rem 1rem;
  background-color: var(--color-primary);
  color: white;
  cursor: pointer;
  border-radius: 0.25rem;
  font-size: 1.25rem;
}

.btns {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(2, 1fr);
}
</style>
