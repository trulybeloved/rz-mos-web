<script setup>
import { RouterView } from 'vue-router'
import TheHeader from './components/TheHeader.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <TheHeader />
    </div>
  </header>

  <RouterView />
</template>

<style scoped></style>
