<template>
    <div class="character-card">
      <div class="category-labels">
        <span v-if="character.category">{{ character.category }}</span>
        <span v-if="character.subcategory"> - </span>
        <span v-if="character.subcategory">{{ character.subcategory }}</span>
      </div>
      <div class="card-header">
        <span class="card-title">{{ character.character }}</span>
      </div>
      <div class="card-body">
        <!-- New data fields -->
        <p v-if="character.relevant"><span class="field-label">Relevant?</span> {{ character.relevant }}</p>
        <p v-if="character.selfReferral"><span class="field-label">Self-referral:</span> {{ character.selfReferral }}</p>
        <p v-if="character.vocabulary"><span class="field-label">Vocabulary:</span> {{ character.vocabulary }}</p>
        <p v-if="character.cussing"><span class="field-label">Cussing:</span> {{ character.cussing }}</p>
        <p v-if="character.feelingOfSpeech"><span class="field-label">Feeling of speech:</span> {{ character.feelingOfSpeech }}</p>
        <p v-if="character.contractions"><span class="field-label">Contractions:</span> {{ character.contractions }}</p>
        <p v-if="character.referralToOthers"><span class="field-label">Referral to others:</span> {{ character.referralToOthers }}</p>
        <p v-if="contractions" v-html="contractions"></p>

        <!-- End of new data fields -->
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
    color: #ececec;
    background-color: #2c2c2c;
    border: 1px solid #393939;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    flex: 1 1 500px;
  }

  .category-labels {
    color: #b1b1b1;
    padding-bottom: 5px;
  }
  
  .card-header {
    background-color: #333;
    color: #e4e4e4;
    font-weight:bold;
    font-size: 25px;
    padding: 5px;
    padding-left: 10px;
    border-radius: 10px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
  }

  .field-label {
    font-weight: lighter;
  }
  
  .card-body {
    padding: 10px;
  }
  
  /* Add more styling as needed */
  </style>
  