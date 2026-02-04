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
    <div class="flex items-center justify-center pb-4">
      <SearchBar v-model="searchTerm" :placeholder="searchBarPlaceholder" />
    </div>
    <div class="flex flex-grow flex-shrink-0 flex-basis-0 justify-end pb-4">
      <RadixSwitch class="switch" @checked="searchAllFields = !searchAllFields" :label="'Search all fields'" />
    </div>

    <div v-if="filteredCharacters.length"
      class="grid grid-cols-[repeat(auto-fit,minmax(400px,1fr))] gap-5 justify-between scroll-smooth max-[450px]:grid-cols-1">
      <div v-for="(characterEntry, index) in filteredCharacters" :key="index"
        class="border rounded-[10px] p-4 min-w-0 text-base"
        style="color: var(--card-color); background-color: var(--card-background-color); border-color: var(--card-border-color);">
        <div class="font-bold py-[5px] px-[10px] pr-[5px] rounded-[10px] rounded-tl-[5px] rounded-tr-[5px]"
          style="background-color: var(--card-header-background-color); color: var(--card-header-color);">
          <div class="text-[1.6rem]">{{ characterEntry.name }}</div>
          <div class="text-[1.1rem] font-[150] brightness-[0.8]">{{ characterEntry.Kanji }} ({{ characterEntry.Romaji
            }})</div>
        </div>

        <div class="p-4 pb-0 brightness-[0.95]">
          {{ characterEntry.description }}
        </div>

        <div v-for="(section, section_title) in characterEntry" :key="section_title" class="section-container">
          <div v-if="!sectionFilterList.includes(section_title) && typeof section === 'object'" class="pt-4 px-4">
            <div class="pl-4 text-[1.1rem] font-[250]">{{ section_title }}</div>
            <div class="p-4 pl-6 rounded-[10px]" style="background-color: var(--card-contents-background-color);">
              <div v-for="(subsection, index) in section" :key="index" class="subsection-container">
                <div v-if="typeof index === 'string'" class="subsection">
                  <div v-if="typeof subsection === 'string'">
                    <span class="font-[250]">{{ index }}: </span>{{ subsection }}
                  </div>

                  <div v-else>
                    <span class="font-[250]">{{ index }}: </span>
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
            <div v-if="!sectionFilterList.includes(section_title) && typeof section === 'string'" class="pt-4 px-4">
              <div class="pl-4 text-[1.1rem] font-[250]">{{ section_title }}</div>
              <div class="p-4 pl-6 rounded-[10px]" style="background-color: var(--card-contents-background-color);">
                <div class="subsection">{{ section }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center p-4 text-[2rem] rounded-[10px]"
      style="background-color: var(--card-contents-background-color);">
      <p>No results</p>
    </div>
  </div>

  <div class="text-center p-4">
    Content sourced from
    <a href="https://rezero.fandom.com/wiki/Re:Zero_Wiki">Re:ZERO Wiki</a>
    under the <a href="https://creativecommons.org/licenses/by-sa/3.0/">CC BY-SA 3.0</a> license
  </div>
</template>