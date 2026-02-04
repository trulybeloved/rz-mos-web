<script lang="js">

const props = defineProps({
    text: {
        type: String,
        required: true
    }
})

</script>

<template>

    <div class="p-2 rounded">
        {{ props.text }}
    </div>

</template>
