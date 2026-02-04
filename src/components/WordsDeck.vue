<script setup>
import SearchBar from './SearchBar.vue'
import { ref, computed, onMounted, watch } from 'vue'
import { makeHttpRequest } from './axiosRequest.js'
import { watchDebounced } from '@vueuse/core'

import { useHighlight } from './useHighlight.js'

const mos_words = await makeHttpRequest(
  '/mos_dictionary_tables.json',
  'https://raw.githubusercontent.com/trulybeloved/rz-mos-web/main/public/mos_dictionary_tables.json'
)

function parseJSON(jsonData) {
  const outerArray = jsonData.map((obj) => {
    const parsedObj = {}
    for (const [key, value] of Object.entries(obj)) {
      const newArray = []
      for (const [key2, value2] of Object.entries(value)) {
        const formattedKey = key2.toLowerCase().replace('cries (for witchbeasts etc)', 'cries').replace('translation', 'tl').replaceAll(/[\s-]+/g, '_')
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
  console.log(parsedData)
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
    const english = wordEntry.english_tl
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
    <div class="flex items-center justify-center pb-7.5">
      <SearchBar v-model="searchTerm" :placeholder="'Search all fields...'" />
    </div>
    <div ref="wordsContainer">
      <div v-if="filteredWords.length" class="grid grid-cols-1 gap-5">
        <div v-for="(wordEntry, index) in filteredWords" :key="index" class="border rounded p-2.5"
          style="color: var(--card-color); background-color: var(--card-background-color); border-color: var(--card-border-color);">
          <div class="p-2">
            <span class="text-[1.8rem]">{{ wordEntry.japanese }} :&nbsp;</span>
            <span class="text-[1.4rem]">{{ wordEntry.english_tl }}</span>
            <div v-if="wordEntry.used_for" class="text-base" style="color: var(--used-for-color);">
              <fieldset class="">
                <legend>Used For:</legend>
                <div v-if="typeof (wordEntry.used_for) === 'string'">Used For: {{ wordEntry.used_for }}</div>
                <div v-else-if="Array.isArray(wordEntry.used_for)" class="flex flex-row gap-1">
                  <p v-for="entry in wordEntry.used_for">{{ entry }}</p>
                </div>
              </fieldset>
            </div>
            <div v-if="wordEntry['prefix/suffix']" class="text-base" style="color: var(--notes-color);">
              Prefix/Suffix: {{ wordEntry['prefix/suffix'].replaceAll('\\n', ' || ') }}
            </div>
            <div v-if="wordEntry.notes" class="text-base" style="color: var(--notes-color);">
              <div v-if="typeof (wordEntry.notes) === 'string'">Notes: {{ wordEntry.notes }}</div>
              <div v-else-if="Array.isArray(wordEntry.notes)">
                Notes: <p v-for="note in wordEntry.notes">{{ note }}</p>
              </div>
            </div>
            <div v-if="wordEntry.cries" class="text-base" style="color: var(--notes-color);">
              <!-- Cries: {{ wordEntry.cries.replaceAll('\\n', ' || ') }} -->
            </div>
            <div v-if="wordEntry.observations" class="text-base" style="color: var(--notes-color);">
              <!-- Observations: {{ wordEntry.observations.replaceAll('\\n', ' || ') }} -->
            </div>
            <div v-if="wordEntry.relevant_characters" class="text-base" style="color: var(--notes-color);">
              <!-- Relevant Characters: {{ wordEntry.relevant_characters.replaceAll('\\n', ' | ') }} -->
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center p-4 text-[2rem] rounded-[10px]"
        style="background-color: var(--card-contents-background-color);">
        <p>No results</p>
      </div>

    </div>

  </div>
</template>