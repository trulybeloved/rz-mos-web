<script setup>
import SearchBar from './SearchBar.vue'
import { ref, computed } from 'vue'
import { makeHttpRequest } from './axiosRequest.js'

const mos_words = await makeHttpRequest(
  'https://storage.googleapis.com/rezero-search-public-assets/manual-of-style-data/manual-of-style-raw.json'
)

function parseJSON(jsonData) {
  
  const outerArray = jsonData.map((obj) => {
    const parsedObj = {}
    for (const [key, value] of Object.entries(obj)) {
      const newArray = []
      for (const [key2, value2] of Object.entries(value)) {
        const formattedKey = key2.toLowerCase().replace(/[\s-]+/g, '_')
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

const filteredWords = computed(() => {

  let filtered = parsedWords.filter((wordEntry) => {
    const japanese = wordEntry.japanese;
    const english = wordEntry.english;
    const usedFor = wordEntry.used_for;
    const notes = wordEntry.notes;

    if (
      (japanese && (typeof japanese === 'string') && japanese.toLowerCase().includes(searchTerm.value.toLowerCase())) ||
      (english && (typeof english === 'string') && english.toLowerCase().includes(searchTerm.value.toLowerCase())) ||
      (usedFor && (typeof usedFor === 'object') && usedFor.toString().toLowerCase().includes(searchTerm.value.toLowerCase())) ||
      (notes && (typeof notes === 'string') && notes.toLowerCase().includes(searchTerm.value.toLowerCase()))
    ) {
      return true;
    } else {
      return false;
    }
  });
  
  return filtered
})

</script>

<template>
  <div>
    <div class="search-container">
      <SearchBar v-model="searchTerm" />
    </div>

    <div class="words-container">
      <div v-for="(wordEntry, index) in filteredWords" :key="index" class="word-entry">
        <div class="word-details">
          <span class="japanese"> {{ wordEntry.japanese }}&nbsp;:&nbsp;</span>
          <span class="english">{{ wordEntry.english }} </span>
          <span v-if="wordEntry.used_for" class="used-for"><br> Used for : |</span> 
          <span v-for="(usedFor, index) in wordEntry.used_for" :key="index" class="used-for">| {{ usedFor }} |</span> 
          <span v-if="wordEntry.used_for" class="used-for">|</span>
          <span v-if="wordEntry.notes" class="notes"><br>Notes: {{ wordEntry.notes }}</span>

        </div>
      </div>
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
  color: #ececec;
  background-color: #2c2c2c;
  border: 1px solid #393939;
  padding: 10px;
  border-radius: 5px;
}

.word-details {
  padding: 0.5rem;
}

.japanese {
  font-size: 2em;
}

.english {
  font-size: 1.4em;
}

.used-for {
  font-size: 1.1em;
  color: #a5a5a5;
}

.notes {
  font-size: 1.1em;
  color: #a5a5a5;
}
</style>
