<script setup lang="ts">
import { useRoute, RouterLink } from 'vue-router'
import { computed } from 'vue'
import type { Book, Comment, Rating, BookIssue, LibrarianIssue } from '@/types'
import BookPlaceholder from '@/components/BookPlaceholder.vue'
import { useStore } from '@/store'
// import AdminToolbar from '@/components/AdminToolbar.vue'
import IssueBook from '@/components/books/modals/IssueBook.vue'
import ReturnBook from '@/components/books/modals/ReturnBook.vue'
import EditBook from '@/components/books/modals/EditBook.vue'
import DeleteBook from '@/components/books/modals/DeleteBook.vue'
import UnissueBook from '@/components/books/modals/UnissueBook.vue'

import IssueRequests from '@/components/books/IssueRequests.vue'
import ActiveIssues from '@/components/books/ActiveIssues.vue'

const store = useStore()

const route = useRoute()
const id = parseInt(route.params.id as string)

const isAuth = computed(() => store.getters.isAuth)
const isLibrarian = computed(() => store.getters.isLibrarian)
const isAdmin = computed(() => store.getters.isAdmin)
const isUser = computed(() => store.getters.isUser)

const issued = computed<boolean>(() => store.getters.issued(id))
const requested = computed<boolean>(() => store.getters.requested(id))

const requests = computed<LibrarianIssue[]>(() => store.getters.issue_requests_by_book(id))
const issues = computed<LibrarianIssue[]>(() => store.getters.active_issues_by_book(id))

const book = computed<Book>(() => store.getters.book(id))
const error = computed(() => !book.value && 'Book not found')

const title = computed(() => book.value?.title)
const description = computed(() => book.value?.description)
const year = computed(() => book.value?.year)
const isbn = computed(() => book.value?.isbn)
const genre = computed(() => book.value?.section?.name)
const author = computed(() => book.value?.author)

const imageUrl = computed(() => (book.value?.image ? `http://localhost:5000/images/${book.value?.image}` : undefined))

// const comments = computed<Comment[]>(() => book.value.comments)

const userRating = computed<Rating>(() => store.getters.rating(id))
const rating = computed(() => (userRating.value?.rating || book.value?.rating || 0).toFixed(1))

const canRead = computed(() => isAuth.value && ((isUser.value && issued.value) || isLibrarian.value))
const canIssue = computed<boolean>(() => isAuth.value && isUser.value && !issued.value && !requested.value)
const canUnissue = computed<boolean>(() => isAuth.value && isUser.value && requested.value && !issued.value)
const canReturn = computed<boolean>(() => isAuth.value && isUser.value && issued.value)
const canModify = computed<boolean>(() => isAdmin.value || isLibrarian.value)

const badge = computed(() => {
  if (!isAuth.value) return ''
  if ((isUser.value && issued.value) || (isLibrarian.value && book.value?.issued)) return 'Issued'
  return 'Available'
})

const badgeClass = computed(() => {
  if (!isAuth.value) return 'available'
  if ((isUser.value && issued.value) || (isLibrarian.value && book.value?.issued)) return 'issued'
  if (isUser.value && requested.value) return 'requested'
  return ''
})

const handleRating = (e: MouseEvent) => {
  const target = e.target as HTMLElement
  const rating = parseInt(target.dataset.rating || '0')
  store.dispatch('rateBook', { book_id: id, rating })
}
</script>

<template>
  <div class="book-view">
    <RouterLink to="/books" class="back-link">Back to books</RouterLink>
    <!-- <AdminToolbar /> -->

    <section class="book">
      <div class="book-card">
        <div class="book-img">
          <BookPlaceholder :src="imageUrl" />
        </div>

        <template v-if="error">
          <h1 class="error">{{ error }}</h1>
          <p class="error-message">The book you are looking for is not available. Please check back later.</p>
        </template>

        <template v-else>
          <h1 v-if="title" class="book-title">{{ title }}</h1>
          <p v-if="description" class="book-description">{{ description }}</p>
          <div class="book-info" v-if="author || year || isbn">
            <p><strong>Author:</strong> {{ author }}</p>
            <p><strong>Year:</strong> {{ year }}</p>
            <p><strong>ISBN:</strong> {{ isbn }}</p>
            <p><strong>Genre:</strong> {{ genre }}</p>
          </div>

          <div class="badge" v-if="badge" :class="badgeClass">{{ badge }}</div>

          <div class="rating-container">
            <div class="rating" :style="{ '--value': rating }" :class="{ active: isUser }">
              <span data-rating="1" @click="handleRating">⭐</span>
              <span data-rating="2" @click="handleRating">⭐</span>
              <span data-rating="3" @click="handleRating">⭐</span>
              <span data-rating="4" @click="handleRating">⭐</span>
              <span data-rating="5" @click="handleRating">⭐</span>
            </div>
            <span> {{ rating }}/5 </span>
          </div>

          <div class="book-actions">
            <RouterLink v-if="canRead" :to="`/read/${id}`" class="button read">Read Book</RouterLink>
            <IssueBook v-if="canIssue" :book="book" />
            <UnissueBook v-if="canUnissue" :book="book" />
            <ReturnBook v-if="canReturn" :book="book" />
            <EditBook v-if="canModify" :book="book" />
            <DeleteBook v-if="canModify" :book="book" />
          </div>

          <!-- <Comments :comments="comments" /> -->

          <template v-if="isLibrarian">
            <IssueRequests :requests="requests" :include_title="false" v-if="requests.length" />
            <ActiveIssues :issues="issues" :include_title="false" v-if="issues.length" />
          </template>
        </template>
      </div>
    </section>
  </div>
</template>

<style scoped>
.book-view {
  display: grid;
  gap: 1rem;

  grid-template-rows: auto 1fr;
  grid-template-columns: auto 1fr;
}

.book {
  display: grid;
  gap: 2rem;

  grid-template-rows: auto auto 1fr;
  grid-column: span 2;
}

.book-card {
  display: grid;
  grid-template-columns: 10rem 1fr auto;
  grid-template-rows: auto auto auto 1fr;
  gap: 0 2rem;

  .book-img {
    border-radius: 1rem;
    grid-column: 1;
    grid-row: span 3;
    border: 4px solid var(--color-primary);
    aspect-ratio: 1 / 1;
    display: grid;
    overflow: hidden;
  }

  .book-title {
    grid-column: 2;
    font-size: 3rem;
  }

  .book-description {
    grid-column: 2 / span 2;
  }

  .book-info {
    grid-column: 2;

    display: flex;
    align-items: center;
    gap: 3rem;
  }

  .badge {
    grid-column: 3;
    grid-row: 1;

    place-self: center end;
  }
}

.error {
  color: var(--color-error);
  align-self: center;
  margin: 0;
  font-size: 3rem;

  grid-row: span 2;
}

.error-message {
  color: var(--color-text-mute);
  font-size: 1.5rem;

  grid-column: 2;
  grid-row: 3;
}

.rating-container {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.5rem;
  grid-column: 3;

  align-items: center;
}

.rating {
  /* --value: 5; */
  --_value: calc(var(--value, 2.5) / 5 * 100%);

  place-self: center;

  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;

  background-image: linear-gradient(90deg, var(--color-primary) var(--_value), var(--color-secondary) var(--_value));

  user-select: none;

  &.active span {
    background-clip: text;
    -webkit-background-clip: text;
    transition: background-color 200ms;
    cursor: pointer;

    &:hover,
    &:has(~ span:hover) {
      background-color: var(--color-primary);
    }

    &:hover ~ span {
      background-color: var(--color-secondary);
    }
  }
}

.book-actions {
  display: flex;
  gap: 2rem;

  padding: 1rem 0;
  border-radius: 0.5rem;
  margin: 1rem 0;

  grid-column: 2 / -1;
}

.requests,
.issues {
  grid-column: 2 / -1;
  margin-top: 1rem;
}
</style>
