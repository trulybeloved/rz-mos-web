<script setup>
import SearchBar from './SearchBar.vue'
import { ref, computed } from 'vue'
import { makeHttpRequest } from './axiosRequest.js'

const wiki_characters = await makeHttpRequest(
  'https://rzmosweb.pages.dev/rz_wiki_character_details.json',
  'https://raw.githubusercontent.com/trulybeloved/rz-mos-web/main/public/rz_wiki_character_details.json'
)

const searchTerm = ref('')

const filteredCharacters = computed(() => {
  let filtered = wiki_characters.filter((characterEntry) => {
    const characterEngName = characterEntry.name
    const characterJapName = characterEntry.kanji

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
  // Sort filtered characters alphabetically based on the .name string
  filtered.sort((a, b) => {
    const nameA = a.name.toLowerCase()
    const nameB = b.name.toLowerCase()
    return nameA < nameB ? -1 : 1
  })

  return filtered
})

const sectionFilterList = ["character_name", "name", "Kanji", "Romaji"]
</script>

<template>
  <div>
    <div class="search-container">
      <SearchBar v-model="searchTerm" />
    </div>

    <div class="card-container">
      <div v-for="(characterEntry, index) in filteredCharacters" :key="index" class="character-card">

        <div class="card-header">
          <div class="card-title">{{ characterEntry.name }}</div>
          <div class="card-subtitle">{{ characterEntry.Kanji }} ({{ characterEntry.Romaji }})</div>
        </div>
        
        <div v-for="(section, section_title) in characterEntry" :key="section_title" class="section-container"> 
            
            <div v-if="!sectionFilterList.includes(section_title) && typeof section === 'object'" class="section">
                <div class="section-title">{{ section_title }}</div> 
                <div class="section-content">
                    
                    <div v-for="(subsection, index) in section" :key="index" class="subsection-container">
                        
                            <div v-if="typeof index === 'string'" class="subsection">
                                <div v-if="(typeof subsection === 'string')">
                                    <span class="field-label">{{ index }}: </span>{{ subsection }}
                                </div>
                                <div v-else >
                                    <span class="field-label">{{ index }}: </span>
                                    <ul>
                                    <li v-for="(subsubsection, index) in subsection" :key="index">
                                        {{ subsubsection }}
                                    </li>
                                    </ul>
                                </div>
                                
                            </div>
                            <div v-else-if="typeof index === 'number'" class="subsection">
                                <ul>
                                <li>{{ subsection }}</li>
                                </ul>
                            </div>   
                    </div>
                    
                </div>
            </div>
            
            <div v-else>
                <div v-if="!sectionFilterList.includes(section_title) && typeof section === 'string'" class="section">
                    <div class="section-title">{{ section_title }}</div> 
                    <div class="section-content">
                        <div class="subsection">{{ section }}</div> 
                    </div>
                </div>  
            </div>
        
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

.card-container {
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

.character-card {
  color: #ececec;
  background-color: #2c2c2c;
  border: 1px solid #393939;
  border-radius: 10px;
  padding: 20px;
  /* width: 100%; */
  min-width: 0;
  font-size: 1.2em;
}

.card-header {
  background-color: #333;
  color: #e4e4e4;
  font-weight: 700;
  padding: 5px;
  padding-left: 10px;
  border-radius: 10px;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
}

.card-title {
  font-size: 1.5em;
}

.card-subtitle {
  font-size: 1em;
  font-weight: 150;
  filter: brightness(80%);
}

.section {
    padding-top: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

.section-title {
    padding-left: 1rem;
    font-size: 1.1em;
    font-weight: 250;
}

.section-content {
    padding: 1rem 1rem 1rem 1.5rem;
    border-radius: 10px;
    background-color: #242424;
}

.field-label {
    font-weight: 250;
}
</style>
