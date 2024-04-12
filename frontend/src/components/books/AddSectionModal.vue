<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { createSection } from '@/utils/api'
import SectionPlaceholder from '@/components/SectionPlaceholder.vue'

const dialog = ref<HTMLDialogElement>()

const section = reactive({
  name: '',
  description: ''
})

const image = ref<HTMLInputElement>()
const imgSrc = ref<string>()

const openModal = () => {
  dialog.value?.showModal()
}

const closeModal = () => {
  dialog.value?.close()
}

const addSection = async () => {
  const { name, description } = section
  console.log(name, description, image.value?.files?.[0].name)
  const newSection = await createSection({
    name,
    description,
    image: image.value?.files?.length ? image.value?.files[0] : null
  })
  console.log(newSection)
  closeModal()
}

onMounted(() => {
  image.value?.addEventListener('change', (e) => {
    const target = e.target as HTMLInputElement
    const file = target.files?.[0]

    if (!file) return

    const reader = new FileReader()
    reader.onload = () => {
      imgSrc.value = reader.result as string
    }
    reader.readAsDataURL(file)
  })
})
</script>

<template>
  <dialog ref="dialog" class="add-section-modal">
    <h2>Add Section</h2>
    <form @submit.prevent="addSection">
      <label>
        Name
        <input v-model="section.name" type="text" required />
      </label>
      <label>
        Description
        <textarea v-model="section.description" required></textarea>
      </label>

      <label for="image" class="image"
        >Image
        <input type="file" id="image" name="image" ref="image" accept="image/*" />
      </label>

      <div class="btns">
        <button type="submit">Add</button>
        <button type="button" @click="closeModal">Cancel</button>
      </div>

      <div class="section-card">
        <SectionPlaceholder :src="imgSrc" />
        <div class="section-card-content">
          <h3 class="name">{{ section.name ? section.name : '--Name--' }}</h3>
          <p class="description">
            {{ section.description ? section.description : '--Description--' }}
          </p>
        </div>
      </div>
    </form>
  </dialog>

  <button class="add-btn" @click="openModal">Add Section</button>
</template>

<style scoped>
.add-section-modal {
  padding: 2rem;

  & form {
    display: grid;
    gap: 1rem 2rem;

    grid-template-rows: auto 1fr auto auto;
    grid-template-columns: 1fr auto;
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
}

h2 {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 1rem;
}

input,
textarea {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
}

.btns {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(2, 1fr);
  grid-column: 1 / -1;
  place-self: end;
  margin-top: 1rem;

  & button {
    padding: 0.5em 1.25em;
    background-color: var(--color-primary);
    color: var(--color-background);
    cursor: pointer;
    border-radius: 0.25rem;
    font-size: 1.25rem;
    font-weight: bold;

    transition: background-color 200ms;

    &:hover {
      background-color: var(--color-primary-dark);
    }
  }
}

.section-card {
  border: 3px solid var(--color-secondary);
  background-color: var(--color-background-mute);
  margin: 2rem 0 1rem;
  border-radius: 0.5rem;

  grid-column: 2;
  grid-row: 1 / span 3;

  width: 16rem;
  /* aspect-ratio: 3 / 4; */

  display: grid;
  gap: 0.5rem;

  overflow: hidden;

  & img {
    width: 100%;
  }

  & .section-card-content {
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

  & .name {
    font-size: 1.25rem;
    font-weight: bold;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;

    grid-column: 1 / -1;
  }

  & .description {
    font-size: 1rem;
  }
}
</style>
