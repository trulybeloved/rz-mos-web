<!-- SearchBar.vue -->
<template>
  <input type="text" v-model="searchTerm" :placeholder="placeholder" class="search-input" />
</template>

<script setup>
import { ref } from 'vue'

const searchTerm = ref('')

defineProps({
  placeholder: {
    type: String,
    required: false
  }
})
</script>

<style scoped>
.search-input {
  display: block;
  color: #ccc;
  background-color: #090909;
  width: 100%;
  padding: 1em;
  border: 1px solid #474747;
  border-radius: 10px;
  font-size: 16px;
  outline: none;
  max-width: 1000px;
}
</style>
