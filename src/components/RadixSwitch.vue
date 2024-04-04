<script setup>
import { SwitchRoot, SwitchThumb } from 'radix-vue'
import { ref } from 'vue'

const switchState = ref(false)

defineEmits (['checked'])

defineProps({
  label: {
    type: String,
    required: false
  }
})

</script>

<template>
  <div :style="{ display: 'flex', alignItems: 'center'}">
    <label class="Label" for="airplane-mode">
      {{ label }}
    </label>
    <SwitchRoot
      id="search-all-fields-switch"
      v-model:checked="switchState"
      @update:checked="$emit('checked')"
      class="SwitchRoot"
    >
      <SwitchThumb
        class="SwitchThumb"
      />
    </SwitchRoot>
  </div>
</template>

<style>

button {
  all: unset;
}

.SwitchRoot {
  width: 42px;
  height: 25px;
  background-color: var(--switch-root-background-color); 
  border-radius: 9999px;
  position: relative;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
}

.SwitchRoot[data-state='checked'] {
  background-color: var(--switch-root-checked-background-color)
}

.SwitchThumb {
  display: block;
  width: 21px;
  height: 21px;
  background-color: var(--switch-thumb-background-color);
  border-radius: 9999px;
  transition: transform 100ms;
  transform: translateX(2px);
  will-change: transform;
}

.SwitchThumb[data-state='checked'] {
  transform: translateX(19px);
}

.Label {
  color: var(--switch-label-color);
  font-size: 15px;
  line-height: 1;
  padding-right: 1em;
}
</style>