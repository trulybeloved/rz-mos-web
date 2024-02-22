<!-- SearchBar.vue -->
<template>
  <input type="text" v-model="searchTerm" placeholder="Search..." class="search-input" />
</template>

<script setup>
import { ref } from 'vue'

const searchTerm = ref('')
</script>

<style scoped>
.search-input {
  display: block;
  color: #ccc;
  background-color: #121212;
  width: 100%;
  padding: 1em;
  border: 1px solid #505050;
  border-radius: 10px;
  font-size: 16px;
  outline: none;
  max-width: 1000px;
}
</style>
