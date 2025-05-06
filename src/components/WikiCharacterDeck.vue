<script setup>
import SearchBar from './SearchBar.vue'
import { ref, computed } from 'vue'
import { makeHttpRequest } from './axiosRequest.js'
import RadixSwitch from './RadixSwitch.vue'
// import { switchState } from './RadixSwitch.vue'

const wiki_characters = await makeHttpRequest(
  'https://rzmosweb.pages.dev/rz_wiki_character_details.json',
  'https://raw.githubusercontent.com/trulybeloved/rz-mos-web/main/public/rz_wiki_character_details.json'
)

const searchTerm = ref('')
const searchAllFields = ref(false)
const searchBarPlaceholder = computed(() => {
  if (searchAllFields.value) {
    return 'Search all fields...'
  } else {
    return 'Search by EN or JP name...'
  }
})

const filteredCharacters = computed(() => {
  let filtered = wiki_characters.filter((characterEntry) => {
    if (searchAllFields.value) {
      var fullCharacterEntryString = JSON.stringify(characterEntry, null, 2)
      fullCharacterEntryString = fullCharacterEntryString.replace(/["']/g, '')

      if (
        fullCharacterEntryString &&
        typeof fullCharacterEntryString === 'string' &&
        fullCharacterEntryString.toLowerCase().includes(searchTerm.value.toLowerCase())
      ) {
        return true
      } else {
        return false
      }
    } else {
      const characterEngName = characterEntry.name
      const characterJapName = characterEntry.Kanji
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

const sectionFilterList = ['character_name', 'name', 'Kanji', 'Romaji', 'description']
</script>

<template>
  <div>
    <div class="search-container">
      <SearchBar v-model="searchTerm" :placeholder="searchBarPlaceholder" />
    </div>
    <div class="search-options">
      <RadixSwitch
        class="switch"
        @checked="searchAllFields = !searchAllFields"
        :label="'Search all fields'"
      />
    </div>

    <div v-if="filteredCharacters.length" class="card-container">
      <div
        v-for="(characterEntry, index) in filteredCharacters"
        :key="index"
        class="character-card"
      >
        <div class="card-header">
          <div class="card-title">{{ characterEntry.name }}</div>
          <div class="card-subtitle">{{ characterEntry.Kanji }} ({{ characterEntry.Romaji }})</div>
        </div>

        <div class="description">
          {{ characterEntry.description }}
        </div>

        <div
          v-for="(section, section_title) in characterEntry"
          :key="section_title"
          class="section-container"
        >
          <div
            v-if="!sectionFilterList.includes(section_title) && typeof section === 'object'"
            class="section"
          >
            <div class="section-title">{{ section_title }}</div>
            <div class="section-content">
              <div v-for="(subsection, index) in section" :key="index" class="subsection-container">
                <div v-if="typeof index === 'string'" class="subsection">
                  <div v-if="typeof subsection === 'string'">
                    <span class="field-label">{{ index }}: </span>{{ subsection }}
                  </div>

                  <div v-else>
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
            <div
              v-if="!sectionFilterList.includes(section_title) && typeof section === 'string'"
              class="section"
            >
              <div class="section-title">{{ section_title }}</div>
              <div class="section-content">
                <div class="subsection">{{ section }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="no-result">
      <p>No results</p>
    </div>
  </div>

  <div class="content-source">
    Content sourced from
    <a href="https://rezero.fandom.com/wiki/Re:Zero_Wiki">Re:ZERO Wiki</a>
    under the <a href="https://creativecommons.org/licenses/by-sa/3.0/">CC BY-SA 3.0</a> license
  </div>
</template>

<style scoped>
.search-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-bottom: 1rem;
}

.search-options {
  display: flex;
  flex-grow: 1;
  flex-shrink: 0;
  flex-basis: 0;
  justify-content: flex-end;
  padding-bottom: 1rem;
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
  color: var(--card-color);
  background-color: var(--card-background-color);
  border: 1px solid var(--card-border-color);
  border-radius: 10px;
  padding: 1rem;
  /* width: 100%; */
  min-width: 0;
  font-size: 1rem;
}

.card-header {
  background-color: var(--card-header-background-color);
  color: var(--card-header-color);
  font-weight: 700;
  padding: 5px;
  padding-left: 10px;
  border-radius: 10px;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
}

.card-title {
  font-size: 1.6rem;
}

.card-subtitle {
  font-size: 1.1rem;
  font-weight: 150;
  filter: brightness(80%);
}

.description {
  padding: 1rem;
  padding-bottom: 0;
  filter: brightness(95%);
}

.section {
  padding-top: 1rem;
  padding-left: 1rem;
  padding-right: 1rem;
}

.section-title {
  padding-left: 1rem;
  font-size: 1.1rem;
  font-weight: 250;
}

.section-content {
  padding: 1rem 1rem 1rem 1.5rem;
  border-radius: 10px;
  background-color: var(--card-contents-background-color);
}

.field-label {
  font-weight: 250;
}

.content-source {
  text-align: center;
  padding: 1rem;
}

.no-result {
  text-align: center;
  padding: 1rem;
  font-size: 2rem;
  border-radius: 10px;
  background-color: var(--card-contents-background-color);
}
</style>
