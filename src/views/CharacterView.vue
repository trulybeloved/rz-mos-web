<script setup>
import CharacterDeck from '@/components/CharacterDeck.vue'
import LoadingStuff from '@/components/LoadingStuff.vue'
</script>

<template>
  <main>
    <Suspense>
      <CharacterDeck />
      <template #fallback>
        <LoadingStuff />
      </template>
    </Suspense>
  </main>
</template>
