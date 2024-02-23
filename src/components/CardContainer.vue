<template>
  <div>
    <div class="search-container">
      <SearchBar v-model="searchTerm" />
    </div>

    <div class="card-container">
      <CharacterCard
        v-for="(character, index) in filteredCharacters"
        :key="index"
        :character="character"
        :contractions="character.contractionData"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    characters: {
      type: Object,
      required: true
    }
  }
}

import CharacterCard from './components/CharacterCard.vue'
import SearchBar from './components/SearchBar.vue' // Import the SearchBar component
import { ref, computed } from 'vue'

// fetch('https://storage.googleapis.com/rezero-search-public-assets/speech-style-data/speech-style-raw-data.json')
//   .then(response => {
//     if (!response.ok) {
//       throw new Error('Network response was not ok');
//     }
//     return response.json();
//   })
//   .then(data => {
//     characters = data;
//     // Work with the JSON data here
//     console.log(data);
//   })
//   .catch(error => {
//     console.error('There was a problem with the fetch operation:', error);
//   });

// function parseJSON(jsonData) {
//     const parsedData = [];
//     for (const obj of jsonData) {
//         const parsedObj = {};
//         const htmlContent = generateHtmlFromJson(obj);
//         for (const [key, value] of Object.entries(obj)) {
//             const formattedKey = key.toLowerCase().replace(/\s+/g, '_');
//             parsedObj[formattedKey] = value;
//         }
//         parsedObj['contractionData'] = htmlContent;
//         parsedData.push(parsedObj);
//     }
//     console.log(parsedData);
//     return parsedData;
// }

function parseJSON(jsonData) {
  const parsedData = []
  jsonData.forEach((obj) => {
    const parsedObj = {}
    const htmlContent = generateHtmlFromJson(obj)
    Object.entries(obj).forEach(([key, value]) => {
      const formattedKey = key.toLowerCase().replace(/\s+/g, '_')
      parsedObj[formattedKey] = value
    })
    parsedObj['contractionData'] = htmlContent
    parsedData.push(parsedObj)
  })
  console.log(parsedData)
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

  // const formattedKeys = keysToInclude.map(key => key.toLowerCase().replace(/\s+/g, '_'));

  let html = '<ul>'
  keysToInclude.forEach((key) => {
    if (data.hasOwnProperty(key) && data[key] !== '') {
      html += `<li>${key} -> </span>${data[key]}</li>`
    }
  })
  html += '</ul>'
  return html
}

const parsedCharacters = parseJSON(characters)

const searchTerm = ref('')

const filteredCharacters = computed(() => {
  // Filter characters based on search term
  let filtered = parsedCharacters.filter((characterEntry) =>
    characterEntry.character.toLowerCase().includes(searchTerm.value.toLowerCase())
  )

  // Sort filtered characters alphabetically based on the .character string
  filtered.sort((a, b) => {
    const nameA = a.character.toLowerCase()
    const nameB = b.character.toLowerCase()
    if (nameA < nameB) return -1
    if (nameA > nameB) return 1
    return 0
  })

  return filtered
})
</script>

<style>
.search-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-bottom: 30px;
}

.card-container {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  flex-direction: row;
  flex-wrap: wrap;
  flex-grow: 1;
  justify-content: center;
  gap: 20px;
  width: 100%;
}
</style>
