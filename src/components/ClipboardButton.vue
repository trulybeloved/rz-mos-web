<template>
    <button @click="copyToClipboard" :class="['btn', buttonStyle]" ref="buttonRef">
      <span v-if="buttonText" class="label"> {{ buttonText }} </span><span class="text-to-copy"> {{ textToCopy }}</span>
    </button>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const props = defineProps({
    buttonText: {
      type: String,
      default: '',
    },
    buttonStyle: {
      type: String,
      default: 'btn-primary',
      validator: (value) => ['btn-primary', 'btn-secondary'].includes(value),
    },
    textToCopy: {
      type: String,
      default: '',
    }
  });

  const buttonRef = ref(null);
  
  // Function to show a tooltip with a message
function showTooltip(element, message) {
  const tooltip = document.createElement("div");
  tooltip.textContent = message;
  tooltip.style.position = "absolute";
  tooltip.style.background = "black";
  tooltip.style.color = "white";
  tooltip.style.padding = "5px 10px";
  tooltip.style.borderRadius = "5px";
  tooltip.style.fontSize = "1rem";
  tooltip.style.whiteSpace = "nowrap";
  tooltip.style.transform = "translateY(-100%)";
  tooltip.style.top = `${element.offsetTop - tooltip.offsetHeight - 10}px`;
  tooltip.style.left = `${element.offsetLeft + element.offsetWidth/4}px`;
  tooltip.style.zIndex = "2000";

  element.parentElement.appendChild(tooltip);

  // Remove the tooltip after 1.2 seconds
  setTimeout(() => {
    tooltip.remove();
  }, 1200); // Remove after 1.2 seconds
};


  const copyToClipboard = () => {
    const textToCopy = props.textToCopy;
    navigator.clipboard.writeText(textToCopy)
      .then(() => {
        // console.log('Text copied to clipboard:', textToCopy);
        showTooltip(buttonRef.value, 'Copied!');
      })
      .catch((error) => {
        console.error('Failed to copy text: ', error);
        showTooltip(buttonRef.value, 'FAILED TO COPY');
      });
  };
  </script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.875em;
  font-weight: 600;
  border-radius: 0.5em;
  padding: 0.5em 1em;
  font-size: 1rem;
  line-height: 1.25em;
  cursor: pointer;
  /* transition: background-color 0.1s ease-in-out, border-color 0.1s ease-in-out, color 0.1s ease-in-out; */
}

@media screen and (max-width: 600px) {
    .btn {
        font-size: 0.8rem;
        transition: font-size 0.5s ease;
    }
    
}

.btn-primary {
  background-color: #2b2b2b;
  color: #e1e1e1;
}

.btn-primary:hover {
  background-color: var(--clipboard-hover-background-color);
}

.btn-primary:active {
  background-color: var(--clipboard-active-background-color);
}

.btn-secondary {
  background-color: #cbd5e1;
  color: #334155;
}

.btn-secondary:hover {
  background-color: #94a3b8;
}

.btn-secondary:focus {
  outline: 2px solid rgba(203, 213, 225, 0.7);
  outline-offset: 2px;
}

.text-to-copy {
    background-color: #000000;
    padding: 0.5em;
    border-radius: 0.5em;
    /* margin-left: 1em; */
}
</style>