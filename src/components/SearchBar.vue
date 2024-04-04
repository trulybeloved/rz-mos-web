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
  color: var(--search-color);
  background-color: var(--search-background-color);
  width: 100%;
  padding: 1em;
  border: 1px solid var(--search-border-color);
  border-radius: 10px;
  font-size: 1rem;
  outline: none;
  max-width: 1000px;
}
</style>
