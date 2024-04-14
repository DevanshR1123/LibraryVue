<script setup lang="ts">
import { ref } from 'vue'
import { useStore } from '@/store'
import { toast } from 'vue3-toastify'
import { useRouter } from 'vue-router'
import type { Section } from '@/types'

const { section } = defineProps<{ section: Section }>()

const router = useRouter()
const store = useStore()

const dialog = ref<HTMLDialogElement>()

const showModal = () => {
  dialog.value!.showModal()
}

const closeModal = () => {
  dialog.value!.close()
}

const deleteSection = async () => {
  try {
    await store.dispatch('deleteSection', section.id)
    if (router.currentRoute.value.name === 'section') router.push('/sections')
  } catch (error) {
    console.error(error)
    toast.error('Failed to delete section')
  }

  closeModal()
}
</script>

<template>
  <dialog ref="dialog" class="issue-section-modal">
    <h2>Delete Section</h2>
    <form @submit.prevent="deleteSection">
      <p>
        Are you sure you want to delete <strong>"{{ section.name }}"</strong> section?
      </p>

      <div class="btns">
        <button type="submit" class="button delete">Delete</button>
        <button type="button" class="button issue" @click="closeModal">Cancel</button>
      </div>
    </form>
  </dialog>

  <button class="button delete" @click="showModal">Delete Section</button>
</template>

<style scoped>
.issue-section-modal {
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
