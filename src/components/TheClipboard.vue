<script setup>
import ClipboardButton from './ClipboardButton.vue';
</script>

<template>
    
    <div class="clipboard">
        <div class="text">Clipboard:&nbsp;</div>
        <div class="button-container">
            <ClipboardButton buttonText="Em dash" textToCopy = "―" />
            <ClipboardButton buttonText="Ellipsis" textToCopy = "…" />
            <ClipboardButton buttonText="Tilde" textToCopy = "~" />
            <ClipboardButton buttonText="Dialogue Tag" textToCopy = ": []" />
            <ClipboardButton buttonText="" textToCopy = "――" />
            <ClipboardButton buttonText="" textToCopy = ": [――――]" />
            <ClipboardButton buttonText="" textToCopy = ": [――Hk!]" />
        </div>
    </div>


</template>

<style scoped>

.text {
    font-weight: 600;
    font-size: 1rem;
    text-align: center;
    padding-bottom: 0.5em;
}

.clipboard {
    display: flex;
    flex-direction: column;
    width: 100%;
    background-color: var(--clipboard-background-color);
    border-radius: 1em;
    padding: 0.5em;
    margin-top: 1em;
}

.button-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 1em;
  flex-wrap: wrap;
  padding-bottom: 1em;
}

@media screen and (max-width: 700px) {
    .text {
        font-size: 0.8rem;
    }
    
}
</style>