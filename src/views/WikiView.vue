<script setup>
import WikiCharacterDeck from '@/components/WikiCharacterDeck.vue'
import LoadingStuff from '@/components/LoadingStuff.vue'
</script>

<template>
  <main>
    <Suspense>
      <WikiCharacterDeck />
      <template #fallback>
        <LoadingStuff />
      </template>
    </Suspense>
  </main>
</template>
