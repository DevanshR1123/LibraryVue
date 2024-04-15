<script setup lang="ts">
import { ref, onMounted, reactive, computed } from 'vue'
import { isValidISBN } from '@/lib/utils'
import BookPlaceholder from '@/components/BookPlaceholder.vue'
import { useStore } from '@/store'
import { toast } from 'vue3-toastify'
import { type NewBook, type Book } from '@/types'

const { book } = defineProps<{
  book: Book
}>()

const store = useStore()
const sections = computed(() => store.state.sections)

const newBook = reactive({
  _year: new Date(new Date().setFullYear(book.year)).toISOString().split('T')[0].split('-').slice(0, 2).join('-'),
  section_id: book.section.id.toString(),
  ...book
})

const content = ref<HTMLInputElement>()
const image = ref<HTMLInputElement>()

const imgSrc = ref<string>(`http://localhost:5000/images/${book.image}`)

const year = computed(() => new Date(newBook._year).getFullYear())

const dialog = ref<HTMLDialogElement>()

const showModal = () => {
  dialog.value!.showModal()
}

const closeModal = () => {
  dialog.value!.close()
}

const addBook = async () => {
  const { title, author, description, isbn } = newBook

  if (!title || !author || !description || !isbn) {
    toast.error('Please fill all the fields')
    return
  }

  if (!isValidISBN(isbn)) {
    toast.error('Invalid ISBN')
    return
  }

  try {
    const bookData: NewBook = {
      title,
      author,
      description,
      isbn,
      year: year.value,
      content: content.value && content.value.files?.[0] ? content.value.files?.[0] : null,
      image: image.value && image.value.files?.[0] ? image.value.files?.[0] : null,
      section_id: parseInt(newBook.section_id || '0')
    }

    await store.dispatch('updateBook', { book_id: book.id, book: bookData })

    // newBook.title = ''
    // newBook.author = ''
    // newBook.description = ''
    // newBook.isbn = ''
    // newBook.section_id = ''
    // newBook._year = new Date().toISOString().split('T')[0].split('-').slice(0, 2).join('-')

    // content.value!.value = ''
    // image.value!.value = ''

    // imgSrc.value = ''
  } catch (error) {
    console.error(error)
    toast.error('Failed to update book')
  }

  closeModal()
}

onMounted(() => {
  image.value!.addEventListener('change', (e) => {
    const target = e.target as HTMLInputElement
    const file = target.files?.[0]

    if (!file) return

    const reader = new FileReader()
    reader.onload = () => {
      imgSrc.value = reader.result as string
    }
    reader.readAsDataURL(file)
  })

  content.value!.addEventListener('change', (e) => {
    const target = e.target as HTMLInputElement
    const file = target.files?.[0]

    if (!file) return

    if (file.type !== 'application/pdf') {
      toast.error('Please select a PDF file')
      target.value = ''
      return
    }

    if (!book.title) newBook.title = file.name.split('.').slice(0, -1).join('.')
  })
})
</script>

<template>
  <dialog ref="dialog" class="book-modal">
    <h2>Add Book</h2>
    <form @submit.prevent="addBook">
      <label for="title" class="title"
        >Title
        <input type="text" id="title" name="title" required v-model="newBook.title" />
      </label>

      <label for="author" class="author"
        >Author
        <input type="text" id="author" name="author" required v-model="newBook.author" />
      </label>

      <label for="isbn" class="isbn"
        >ISBN
        <input type="text" id="isbn" name="isbn" required v-model="newBook.isbn" />
      </label>

      <label for="year" class="year"
        >Year
        <input type="month" id="year" name="year" required v-model="newBook._year" />
      </label>

      <label for="section" class="section"
        >Section
        <select id="section" name="section" required v-model="newBook.section_id" v-if="sections.length">
          <option value="" disabled selected>Select a section</option>
          <option v-for="section in sections" :key="section.id" :value="section.id">
            {{ section.name }}
          </option>
        </select>
        <div class="no-sections" v-else>
          <p>Please create a section first</p>
        </div>
      </label>

      <label for="description" class="description"
        >Description
        <textarea id="description" name="description" required v-model="newBook.description"></textarea>
      </label>

      <label for="image" class="image"
        >Image
        <input type="file" id="image" name="image" ref="image" accept="image/*" />
      </label>

      <label for="content" class="content"
        >Content
        <input type="file" id="content" name="content" ref="content" accept="application/pdf" />
      </label>

      <div class="btns">
        <button type="submit" class="button save">Save</button>
        <button type="button" class="button cancel" @click="closeModal">Cancel</button>
      </div>

      <div class="book-card">
        <BookPlaceholder :src="imgSrc" />
        <div class="book-card-content">
          <h3 class="title">{{ book.title ? book.title : '--Title--' }}</h3>
          <p class="author">{{ book.author ? book.author : '--Author--' }}</p>
          <p class="year">{{ year ? year : '--Year--' }}</p>
        </div>
      </div>
    </form>
  </dialog>

  <button class="button edit" @click="showModal">Edit Book</button>
</template>

<style scoped>
.book-modal {
  padding: 2rem;

  & form {
    display: grid;
    gap: 1rem;
    grid-template-columns: 1fr 1fr auto;
  }

  & label {
    display: grid;
    gap: 0.25em;
    font-size: 0.875rem;
    font-weight: bold;

    grid-template-rows: auto 1fr;
  }

  & input {
    padding: 0.5rem;
    font-size: 1rem;

    &[type='file'] {
      border: 2px solid var(--color-primary);
      border-radius: 0.25rem;
      align-self: center;
    }

    &[type='file']::-webkit-file-upload-button {
      background-color: var(--color-primary);
      color: white;
      padding: 0.25rem 0.75rem;
      border-radius: 0.25rem;
      cursor: pointer;
      border: none;
      margin-right: 1rem;
    }

    &[type='file']::-webkit-file-upload-button:hover {
      background-color: var(--color-primary-dark);
    }
  }

  & textarea {
    padding: 0.5rem;
    font-size: 1rem;
    resize: vertical;
  }

  & select {
    padding: 0.5rem;
    font-size: 1rem;
    align-self: start;
  }

  & .img-wrapper {
    display: grid;
    border: 2px solid var(--color-primary);
    border-radius: 0.25rem;
    place-items: center;

    grid-column: 3;
    grid-row: 1 / span 4;

    & img {
      max-width: 100%;
      border-radius: 0.25rem;
      object-fit: contain;

      height: 6rem;
    }
  }

  & .no-sections {
    font-size: 1rem;
    color: var(--color-error-dark);
    font-weight: normal;
    place-self: center;
  }
}

h2 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  grid-column: 1 / -1;
}

.btns {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(2, 1fr);
  grid-column: 3;
  margin-top: 1rem;
}

.book-card {
  border: 3px solid var(--color-secondary);
  background-color: var(--color-background-mute);
  margin: 2rem 0 1rem 1rem;
  border-radius: 0.5rem;

  grid-column: 3;
  grid-row: 1 / span 4;

  width: 16rem;
  /* aspect-ratio: 3 / 4; */

  place-self: center;

  display: grid;
  gap: 0.5rem;
  grid-template-rows: 3fr 1fr;

  overflow: hidden;

  & img {
    width: 100%;
  }

  & .book-card-content {
    padding: 0 0.75rem 1rem;
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 0.25rem;
  }

  & p {
    font-size: 0.875rem;
    color: var(--color-text-mute);
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }

  & .title {
    font-size: 1.25rem;
    font-weight: bold;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;

    grid-column: 1 / -1;
  }

  & .author {
    font-size: 1rem;
  }

  & .year {
    font-size: 0.875rem;
    text-align: right;
  }
}
</style>
