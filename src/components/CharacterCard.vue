<template>
  <div class="character-card">
    <div class="category-labels">
      <span v-if="character.category">{{ character.category }}</span>
      <span v-if="character.subcategory"> - </span>
      <span v-if="character.subcategory">{{ character.subcategory }}</span>
    </div>
    <div class="card-header">
      <span class="card-title">{{ character.character }}</span>
      <span class="card-subtitle"><br />{{ character.name_in_jp }}</span>
    </div>
    <div class="card-body">
      <div class="character-notes">
        <div v-if="character.japanese_speech_quirks && character.japanese_speech_quirks.length">
          <span class="field-label">Japanese Quirks:<br /></span>
          <div class="note-list">
            <ul>
              <li v-for="(quirk, index) in character.japanese_speech_quirks" :key="index">
                <span>{{ quirk }}</span>
              </li>
            </ul>
          </div>
        </div>

        <div v-if="character.english_speech_quirks && character.english_speech_quirks.length">
          <span class="field-label">English Quirks:<br /></span>
          <div class="note-list">
            <ul>
              <li v-for="(quirk, index) in character.english_speech_quirks" :key="index">
                <span>{{ quirk }}</span>
              </li>
            </ul>
          </div>
        </div>

        <div v-if="character.notes && character.notes.length">
          <span class="field-label">Notes:<br /></span>
          <div class="note-list">
            <ul>
              <li v-for="(quirk, index) in character.notes" :key="index">
                <span>{{ quirk }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="speech-style">
        <p v-if="character.self_referral">
          <span class="field-label">Self-referral:</span> {{ character.self_referral }}
        </p>
        <p v-if="character.vocabulary">
          <span class="field-label">Vocabulary:</span> {{ character.vocabulary }}
        </p>
        <p v-if="character.cussing">
          <span class="field-label">Cussing:</span> {{ character.cussing }}
        </p>
        <p v-if="character.feeling_of_speech">
          <span class="field-label">Feeling of speech:</span> {{ character.feeling_of_speech }}
        </p>
        <p v-if="character.referral_to_others">
          <span class="field-label">Referral to others:</span> {{ character.referral_to_others }}
        </p>
        <p v-if="character.contractions">
          <span class="field-label">Contractions:</span> {{ character.contractions }}
        </p>
        <p v-if="contractions" v-html="contractions"></p>
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

<style scoped>
.character-card {
  color: var(--card-color);
  background-color: var(--card-background-color);
  border: 1px solid var(--card-border-color);
  border-radius: 10px;
  padding: 20px;
  min-width: 0;
  font-size: 1rem;
}

@media screen and (max-width: 750px) {
  .character-card {
    padding: 14px;
  }
}

.category-labels {
  color: var(--category-label-color);
  padding-bottom: 5px;
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
  font-size: 1.5rem;
}

.card-subtitle {
  font-size: 1rem;
  font-weight: 150;
  filter: brightness(80%);
}

.character-notes {
  padding-top: 10px;
  
}

.character-notes div {
  padding-top: 5px;
  padding-bottom: 5px;
}

.note-list {
  list-style-type: disc;
  list-style-position: outside;
  background-color: var(--card-contents-background-color);
  padding: 10px 10px 10px 0px;
  border-radius: 10px;
  font-size: 1rem;
  line-height: 1.5;
  color: var(--card-contents-color);
  text-align: left;
  text-anchor: middle;
}

.note-list ul li {
  padding-top: 5px;
  padding-bottom: 5px;
}

.speech-style {
  padding-top: 5px;
}

.field-label {
  font-weight: 250;
  font-size: 1rem;
  color: var(--card-color);
}

.card-body {
  padding: 10px;
}
.speech-style p {
  padding-top: 5px;
}
</style>
