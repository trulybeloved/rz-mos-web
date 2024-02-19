<script setup>
import SearchBar from './SearchBar.vue'; 
import { ref, computed } from 'vue';
import { makeHttpRequest } from './axiosRequest.js';

const mos_words = await makeHttpRequest('https://storage.googleapis.com/rezero-search-public-assets/manual-of-style-data/manual-of-style.json')

function parseJSON(jsonData) {
    const parsedData = [];

    for (const [key, value] of Object.entries(jsonData)) {
        // console.log(key, value);
        const parsedObj = {};
        parsedObj[key] = value;
        parsedData.push(parsedObj);
    }
    return parsedData;}

const parsedWords = parseJSON(mos_words);

const searchTerm = ref('');

const filteredWords = computed(() => {
  let filtered = parsedWords.filter(wordEntry => {
    return Object.entries(wordEntry).some(([key, value]) =>
      key.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
      value.toLowerCase().includes(searchTerm.value.toLowerCase())
    );
  });
  return filtered;
});

</script>

<template>
    <div>
        <div class="search-container">
        <SearchBar v-model="searchTerm" />
        </div>

        <div class="words-container">
            <div v-for="(word, index) in filteredWords" :key="index" class="word-entry">
                <div v-for="(en, jp) in word" :key="jp" class="word-pair">
                    <span class="japnaese">{{ jp }}</span>: <span class="english">{{ en }}</span>
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

.word-pair {
    font-size: 20px;
    padding: 10px;
}

.japnaese {

}

</style>