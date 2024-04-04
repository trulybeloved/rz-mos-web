<script setup>
import CharacterCard from './CharacterCard.vue'
import SearchBar from './SearchBar.vue' // Import the SearchBar component
import { ref, computed } from 'vue'
// import characters from './assets/speech-style-raw-data.json';
import { makeHttpRequest } from './axiosRequest.js'

const characters = await makeHttpRequest(
  'https://storage.googleapis.com/rezero-search-public-assets/speech-style-data/speech-style-raw-data.json',
  'https://raw.githubusercontent.com/trulybeloved/rz-mos-web/main/public/speech-style-raw-data.json'
)

const characterNotes = await makeHttpRequest(
  'https://rzmosweb.pages.dev/mos_character_notes.json'
)

function parseJSON(jsonData) {
  const parsedData = []
  for (const obj of jsonData) {
    const parsedObj = {}
    const htmlContent = generateHtmlFromJson(obj)
    for (const [key, value] of Object.entries(obj)) {
      const formattedKey = key.toLowerCase().replace(/[\s-]+/g, '_')
      parsedObj[formattedKey] = value
    }
    parsedObj['contractionData'] = htmlContent
    parsedData.push(parsedObj)
  }
  return parsedData
}

function generateHtmlFromJson(data) {
  const keysToInclude = [
    'To',
    'Will',
    'Contracted negative followed by "you"',
    'Words ending in -ing',
    "isn't it?",
    'You',
    'Your(self/selves)',
    'You are',
    '(You) are not',
    'You all / You know',
    'To have',
    'Little',
    'About',
    'Because',
    '(Al)though',
    'Alright',
    'Kind of / Sort of',
    'Going to / Want to',
    'Have to',
    "Don't know",
    'Should have',
    'Let me',
    'Them',
    'And',
    'Probably'
  ]

  let html = '<ul>'
  keysToInclude.forEach((key) => {
    if (data[key]) {
      html += `<li><span class="field-label" style="font-weight: 250;">"${key} -> </span>${data[key]}</li>`
    }
  })
  html += '</ul>'
  return html
}

const parsedCharacters = parseJSON(characters)

function mergeCharacterDataArrays(arr1, arr2, key) {
  const map = new Map()
  arr1.forEach((obj) => {
    map.set(obj[key], obj)
  })

  arr2.forEach((obj) => {
    const keyValue = obj[key]
    if (map.has(keyValue) && obj) {
      Object.assign(map.get(keyValue), obj)
    } else {
      arr1.push(obj)
    }
  })

  return arr1
}

const mergedArray = mergeCharacterDataArrays(parsedCharacters, characterNotes, 'character')

const searchTerm = ref('')

const filteredCharacters = computed(() => {
  let filtered = mergedArray.filter((characterEntry) => {
    const characterEngName = characterEntry.character
    const characterJapName = characterEntry.name_in_jp

    if (
      (characterEngName &&
        typeof characterEngName === 'string' &&
        characterEngName.toLowerCase().includes(searchTerm.value.toLowerCase())) ||
      (characterJapName &&
        typeof characterJapName === 'string' &&
        characterJapName.toLowerCase().includes(searchTerm.value.toLowerCase()))
    ) {
      return true
    } else {
      return false
    }
  })

  // Sort filtered characters alphabetically based on the .character string
  filtered.sort((a, b) => {
    const nameA = a.character.toLowerCase()
    const nameB = b.character.toLowerCase()
    return nameA < nameB ? -1 : 1
  })

  return filtered
})
</script>

<template>
  <div>
    <div class="search-container">
      <SearchBar v-model="searchTerm" :placeholder="'Search by EN or JP name...'" />
    </div>

    <div v-if="filteredCharacters.length" class="card-container">
      <CharacterCard
        v-for="(character, index) in filteredCharacters"
        :key="index"
        :character="character"
        :contractions="character.contractionData"
      />
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

.card-container {
  display: none;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  grid-gap: 20px;
  justify-content: space-between;
  scroll-behavior: smooth;
}

@media screen and (max-width: 450px) {
  .card-container {
    grid-template-columns: 1fr;
  }
}

.no-result {
  text-align: center;
  padding: 1rem;
  font-size: 2em;
  border-radius: 10px;
  background-color: var(--card-contents-background-color);
}

</style>
