<script setup>
import CharacterCard from './CharacterCard.vue';
import SearchBar from './SearchBar.vue'; // Import the SearchBar component
import { ref, computed } from 'vue';
// import characters from './assets/speech-style-raw-data.json';
import { makeHttpRequest } from './axiosRequest.js';

const characters = await makeHttpRequest('https://storage.googleapis.com/rezero-search-public-assets/speech-style-data/speech-style-raw-data.json')

function parseJSON(jsonData) {
    const parsedData = [];
    for (const obj of jsonData) {
        const parsedObj = {};
        const htmlContent = generateHtmlFromJson(obj);
        for (const [key, value] of Object.entries(obj)) {
            const formattedKey = key.toLowerCase().replace(/[\s-]+/g, '_');
            parsedObj[formattedKey] = value;
        }
        parsedObj['contractionData'] = htmlContent;
        parsedData.push(parsedObj);
    }
    console.log(parsedData);
    return parsedData;
}

function generateHtmlFromJson(data) {
    const keysToInclude = [
        "To",
        "Will",
        "Contracted negative followed by \"you\"",
        "Words ending in -ing",
        "isn't it?",
        "You",
        "Your(self/selves)",
        "You are",
        "(You) are not",
        "You all / You know",
        "To have",
        "Little",
        "About",
        "Because",
        "(Al)though",
        "Alright",
        "Kind of / Sort of",
        "Going to / Want to",
        "Have to",
        "Don't know",
        "Should have",
        "Let me",
        "Them",
        "And",
        "Probably"
    ];

    // const formattedKeys = keysToInclude.map(key => key.toLowerCase().replace(/\s+/g, '_'));

    let html = "<ul>";
    keysToInclude.forEach(key => {
        if (data[key]) {
            html += `<li><span class="field-label" style="font-weight: 150;">"${key} -> </span>${data[key]}</li>`;
        }
    });
    html += "</ul>";
    return html;
}

const parsedCharacters = parseJSON(characters);

const searchTerm = ref('');

const filteredCharacters = computed(() => {
  // Filter characters based on search term
  let filtered = parsedCharacters.filter(characterEntry =>
    characterEntry.character.toLowerCase().includes(searchTerm.value.toLowerCase())
  );

  // Sort filtered characters alphabetically based on the .character string
  filtered.sort((a, b) => {
    const nameA = a.character.toLowerCase();
    const nameB = b.character.toLowerCase();
    return (nameA < nameB) ? -1 : 1;
  });

  return filtered;
});
</script>

<template>
  <div>
    <div class="search-container">
      <SearchBar v-model="searchTerm" />
    </div>


    <div class="card-container">
      <CharacterCard v-for="(character, index) in filteredCharacters" :key="index" :character="character" :contractions="character.contractionData" />
    </div>
  </div>
</template>

<style>
.search-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-bottom: 30px;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  grid-gap: 20px;
  justify-content: space-between;
}
</style>
