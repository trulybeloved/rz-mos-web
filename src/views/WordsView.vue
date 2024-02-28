<script setup>
import WordsDeck from '@/components/WordsDeck.vue'
import LoadingStuff from '@/components/LoadingStuff.vue'
</script>

<template>
  <main>
    <Suspense>
      <WordsDeck />
      <template #fallback>
        <LoadingStuff />
      </template>
    </Suspense>
  </main>
</template>
