<template>
  <div class="border rounded-[10px] p-5 min-w-0 text-base max-[750px]:p-[14px]"
    style="color: var(--card-color); background-color: var(--card-background-color); border-color: var(--card-border-color);">
    <div class="pb-[5px]" style="color: var(--category-label-color);">
      <span v-if="character.category">{{ character.category }}</span>
      <span v-if="character.subcategory"> - </span>
      <span v-if="character.subcategory">{{ character.subcategory }}</span>
    </div>
    <div
      class="flex w-full justify-between font-bold py-[5px] px-[10px] pr-[5px] rounded-[10px] rounded-tl-[5px] rounded-tr-[5px]"
      style="background-color: var(--card-header-background-color); color: var(--card-header-color);">
      <div class="flex flex-grow flex-basis-full">
        <span class="text-[1.5rem]">{{ character.character }}</span>
        <span class="pl-2 text-[1.25rem]" v-if="character.name_suffix">{{ character.name_suffix }}</span>
        <span class="text-base font-[150] brightness-[0.8]"><br />{{ character.name_in_jp }}</span>
      </div>
      <div class="flex flex-grow-0 flex-shrink-0 justify-center items-center">
        <div v-if="character.wip" class="flex p-2 justify-center items-center rounded-[5px] bg-black/[0.11]">WIP</div>
      </div>
    </div>
    <div class="p-[10px]">
      <div class="pt-[10px]">
        <div v-if="character.japanese_speech_quirks && character.japanese_speech_quirks.length" class="py-[5px]">
          <span class="font-[250] text-base" style="color: var(--card-color);">Japanese Quirks:<br /></span>
          <div class="list-disc list-outside rounded-[10px] py-[10px] px-[10px] pr-0 text-base leading-6 text-left"
            style="background-color: var(--card-contents-background-color); color: var(--card-contents-color);">
            <ul>
              <li v-for="(quirk, index) in character.japanese_speech_quirks" :key="index" class="py-[5px]">
                <span>{{ quirk }}</span>
              </li>
            </ul>
          </div>
        </div>

        <div v-if="character.english_speech_quirks && character.english_speech_quirks.length" class="py-[5px]">
          <span class="font-[250] text-base" style="color: var(--card-color);">English Quirks:<br /></span>
          <div class="list-disc list-outside rounded-[10px] py-[10px] px-[10px] pr-0 text-base leading-6 text-left"
            style="background-color: var(--card-contents-background-color); color: var(--card-contents-color);">
            <ul>
              <li v-for="(quirk, index) in character.english_speech_quirks" :key="index" class="py-[5px]">
                <span>{{ quirk }}</span>
              </li>
            </ul>
          </div>
        </div>

        <div v-if="character.notes && character.notes.length" class="py-[5px]">
          <span class="font-[250] text-base" style="color: var(--card-color);">Notes:<br /></span>
          <div class="list-disc list-outside rounded-[10px] py-[10px] px-[10px] pr-0 text-base leading-6 text-left"
            style="background-color: var(--card-contents-background-color); color: var(--card-contents-color);">
            <ul>
              <li v-for="(quirk, index) in character.notes" :key="index" class="py-[5px]">
                <span>{{ quirk }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="pt-[5px]">
        <p v-if="character.self_referral" class="pt-[5px]">
          <span class="font-[250] text-base" style="color: var(--card-color);">Self-referral:</span> {{
            character.self_referral }}
        </p>
        <p v-if="character.vocabulary" class="pt-[5px]">
          <span class="font-[250] text-base" style="color: var(--card-color);">Vocabulary:</span> {{
            character.vocabulary }}
        </p>
        <p v-if="character.cussing" class="pt-[5px]">
          <span class="font-[250] text-base" style="color: var(--card-color);">Cussing:</span> {{ character.cussing }}
        </p>
        <p v-if="character.feeling_of_speech" class="pt-[5px]">
          <span class="font-[250] text-base" style="color: var(--card-color);">Feeling of speech:</span> {{
            character.feeling_of_speech }}
        </p>
        <p v-if="character.referral_to_others" class="pt-[5px]">
          <span class="font-[250] text-base" style="color: var(--card-color);">Referral to others:</span> {{
            character.referral_to_others }}
        </p>
        <p v-if="character.contractions" class="pt-[5px]">
          <span class="font-[250] text-base" style="color: var(--card-color);">Contractions:</span> {{
            character.contractions }}
        </p>
        <p v-if="contractions" v-html="contractions" class="pt-[5px]"></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    character: {
      type: Object,
      required: true
    },
    contractions: {
      type: String,
      required: false
    }
  }
}
</script>