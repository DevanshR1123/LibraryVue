<script setup lang="ts">
// import { computed } from 'vue'
import { useStore } from '@/store'
import type { UserStats } from '@/types'

const store = useStore()

const stats: UserStats = await store.dispatch('getUserStats')
</script>

<template>
  <div class="dashboard">
    <div class="summary-statistics">
      <div class="statistic">
        <span>Currently Issued Books:</span>
        <span>{{ stats.total_issues }}</span>
      </div>

      <div class="statistic">
        <span>Total Books Issued:</span>
        <span>{{ stats.total_books }}</span>
      </div>

      <div class="statistic">
        <span>Sections Explored:</span>
        <span>{{ stats.total_sections }}</span>
      </div>
    </div>

    <div class="top-5">
      <div class="top-5-books">
        <table class="table">
          <caption>
            Top 5 Books
          </caption>
          <thead>
            <tr>
              <th>Book</th>
              <th>Times Issued</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in stats.top_5_most_issued_books" :key="book.title">
              <td>{{ book.title }}</td>
              <td>{{ book.count }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="top-5-sections">
        <table class="table">
          <caption>
            Top 5 Sections
          </caption>
          <thead>
            <tr>
              <th>Section</th>
              <th>Times Issued</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="section in stats.top_5_most_issued_sections" :key="section.section">
              <td>{{ section.section }}</td>
              <td>{{ section.count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
<style scoped>
.dashboard {
  display: grid;
  gap: 1rem;
}

.summary-statistics {
  display: flex;
  border: 4px solid var(--color-secondary);
  border-radius: 1rem;
  padding: 1rem;
  gap: 1rem;

  justify-content: space-between;

  & .statistic {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    grid-row: 2;

    & span {
      font-size: 1.25rem;

      &:first-child {
        font-weight: bold;
      }
    }
  }

  & h3 {
    font-size: 1.5rem;
    place-self: start;
  }
}

.graphs {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr 1fr;

  & .graph {
    border: 4px solid var(--color-secondary);
    border-radius: 1rem;
    /* padding: 1rem; */
    overflow: hidden;
    display: grid;

    & img {
      width: 100%;
      height: auto;
    }
  }
}

.top-5 {
  display: grid;
  gap: 1rem;
  grid-template-columns: 2fr 1fr;
  border: 4px solid var(--color-secondary);
  border-radius: 1rem;
  padding: 1rem;
}

.table {
  width: 100%;
  border-collapse: collapse;
  border: 2px solid var(--color-secondary);

  & th,
  & td {
    border: 1px solid var(--color-secondary);
    padding: 0.5rem;
  }

  & th {
    background-color: var(--color-secondary);
    color: var(--text-dark-1);
  }

  & caption {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    font-weight: bold;
    text-align: left;
  }

  & tbody tr:nth-child(even) {
    background-color: var(--color-secondary-light);
    color: var(--text-dark-1);
  }
}
</style>
