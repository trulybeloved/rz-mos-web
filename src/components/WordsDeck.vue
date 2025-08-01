<script setup>
import SearchBar from './SearchBar.vue'
import { ref, computed, onMounted, watch } from 'vue'
import { makeHttpRequest } from './axiosRequest.js'
import { watchDebounced } from '@vueuse/core'

import { useHighlight } from './useHighlight.js'

const mos_words = await makeHttpRequest(
  'https://storage.googleapis.com/rezero-search-public-assets/manual-of-style-data/manual-of-style-raw.json',
  'https://raw.githubusercontent.com/trulybeloved/rz-mos-web/main/public/manual-of-style-raw.json'
)

function parseJSON(jsonData) {
  const outerArray = jsonData.map((obj) => {
    const parsedObj = {}
    for (const [key, value] of Object.entries(obj)) {
      const newArray = []
      for (const [key2, value2] of Object.entries(value)) {
        const formattedKey = key2.toLowerCase().replace('cries (for witchbeasts etc)', 'cries').replaceAll(/[\s-]+/g, '_')
        newArray[formattedKey] = value2
      }
      parsedObj[key] = newArray
    }
    return parsedObj
  })

  const parsedData = []
  outerArray.forEach((obj) => {
    for (const [, value] of Object.entries(obj)) {
      parsedData.push(value)
    }
  })
  return parsedData
}

const parsedWords = parseJSON(mos_words)

const searchTerm = ref('')
const wordsContainer = ref(null)

const { initializeMarker, highlight, unmark, isHighlighting } = useHighlight({
  className: 'custom-highlight'
})

onMounted(() => {
  initializeMarker(wordsContainer.value)
})

const filteredWords = computed(() => {
  let filtered = parsedWords.filter((wordEntry) => {
    const japanese = wordEntry.japanese
    const english = wordEntry.english
    const usedFor = wordEntry.used_for
    const notes = wordEntry.notes
    const cries = wordEntry.cries
    const relevant_characters = wordEntry.relevant_characters


    if (
      (japanese &&
        typeof japanese === 'string' &&
        japanese.toLowerCase().includes(searchTerm.value.toLowerCase())) ||
      (english &&
        typeof english === 'string' &&
        english.toLowerCase().includes(searchTerm.value.toLowerCase())) ||
      (usedFor &&
        typeof usedFor === 'object' &&
        usedFor.toString().toLowerCase().includes(searchTerm.value.toLowerCase())) ||
      (notes &&
        typeof notes === 'string' &&
        notes.toLowerCase().includes(searchTerm.value.toLowerCase())) ||
      (cries &&
        typeof cries === 'string' && (searchTerm.value.toLowerCase().includes('cries') || searchTerm.value.toLowerCase().includes('cry') || 'cries'.includes(searchTerm.value.toLowerCase()) ||
          cries.toLowerCase().includes(searchTerm.value.toLowerCase()))) ||
      (relevant_characters &&
        typeof relevant_characters === 'string' &&
        relevant_characters.toLowerCase().includes(searchTerm.value.toLowerCase()))
    ) {
      return true
    } else {
      return false
    }
  })

  return filtered
})

watchDebounced(filteredWords, () => {
  if (searchTerm.value.trim()) {
    highlight(searchTerm.value)
  } else {
    unmark()
  }
}, { debounce: 50 })
</script>

<template>
  <div>
    <div class="search-container">
      <SearchBar v-model="searchTerm" :placeholder="'Search all fields...'" />
    </div>

    <div v-if="filteredWords.length" class="words-container" ref="wordsContainer">
      <div v-for="(wordEntry, index) in filteredWords" :key="index" class="word-entry">
        <div class="word-details">
          <span class="japanese">{{ wordEntry.japanese }} :&nbsp;</span>
          <span class="english">{{ wordEntry.english }}</span>
          <div v-if="wordEntry.used_for" class="used-for">
            <span>Used for : |</span>
            <span v-for="(usedFor, index) in wordEntry.used_for" :key="index" class="used-for-item">| {{ usedFor }}
              |</span>
            <span>|</span>
          </div>
          <div v-if="wordEntry['prefix/suffix']" class="notes">
            Prefix/Suffix: {{ wordEntry['prefix/suffix'].replaceAll('\\n', ' || ') }}
          </div>
          <div v-if="wordEntry.notes" class="notes">
            Notes: {{ wordEntry.notes.replaceAll('\\n', ' || ') }}
          </div>
          <div v-if="wordEntry.cries" class="notes">
            Cries: {{ wordEntry.cries.replaceAll('\\n', ' || ') }}
          </div>
          <div v-if="wordEntry.observations" class="notes">
            Observations: {{ wordEntry.observations.replaceAll('\\n', ' || ') }}
          </div>
          <div v-if="wordEntry.relevant_characters" class="notes">
            Relevant Characters: {{ wordEntry.relevant_characters.replaceAll('\\n', ' | ') }}
          </div>
        </div>
      </div>
    </div>

    <div v-else class="no-result">
      <p>No results</p>
    </div>
  </div>
</template>

<style scoped>
.search-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-bottom: 30px;
}

.words-container {
  display: grid;
  grid-template-columns: 1fr;
  grid-gap: 20px;
  justify-content: space-between;
}

.word-entry {
  color: var(--card-color);
  background-color: var(--card-background-color);
  border: 1px solid var(--card-border-color);
  padding: 10px;
  border-radius: 5px;
}

.word-details {
  padding: 0.5rem;
}

.japanese {
  font-size: 1.8rem;
}

.english {
  font-size: 1.4rem;
}

.used-for {
  font-size: 1rem;
  color: var(--used-for-color);
}

.notes {
  font-size: 1rem;
  color: var(--notes-color);
}

.no-result {
  text-align: center;
  padding: 1rem;
  font-size: 2rem;
  border-radius: 10px;
  background-color: var(--card-contents-background-color);
}
</style>
