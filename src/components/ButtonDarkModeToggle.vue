<template>
    <div
        :class="[
            'generic-button',
            'dark-mode-toggle-button',
            props.customClass,
        ]"
        :style="props.customStyles"
        @click="handleClick"
    >
        <div class="button-content">
            <span v-if="props.buttonText">{{ props.buttonText }}</span>
            <svg
                width="20px"
                height="20px"
                viewBox="0 0 24 24"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink"
            >
                <desc></desc>
                <g
                    id="🔍-Product-Icons"
                    stroke="none"
                    stroke-width="1"
                    fill="none"
                    fill-rule="evenodd"
                >
                    <g
                        id="ic_fluent_dark_theme_24_regular"
                        :fill="useDarkMode ? '#FFFFFF' : '#000000'"
                        fill-rule="nonzero"
                    >
                        <path
                            d="M12,22 C17.5228475,22 22,17.5228475 22,12 C22,6.4771525 17.5228475,2 12,2 C6.4771525,2 2,6.4771525 2,12 C2,17.5228475 6.4771525,22 12,22 Z M12,20.5 L12,3.5 C16.6944204,3.5 20.5,7.30557963 20.5,12 C20.5,16.6944204 16.6944204,20.5 12,20.5 Z"
                            id="🎨-Color"
                        ></path>
                    </g>
                </g>
            </svg>
        </div>
    </div>
</template>

<script setup>
import { computed } from "vue";
import { useGeneralStore } from "@/store/general";

const generalStore = useGeneralStore();

const useDarkMode = computed(() => {
    return generalStore.getDarkMode;
});

const emit = defineEmits(["click"]);

const props = defineProps({
    customClass: {
        type: String,
        default: "",
    },
    buttonText: {
        type: String,
        default: "",
    },
    customStyles: {
        type: Object,
        default: () => ({}),
    },
    svgIcon: {
        type: [String, Object],
        default: "",
    },
});

const handleClick = () => {
    emit("click");
};
</script>

<style type="scss" scoped>
.button-content {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    overflow: hidden;
}

.generic-button {
    display: flex;
    align-items: center;
    justify-content: center;
    max-width: 52px;
    height: 36px;
    padding: 0.5rem 1rem;
    border: 1px solid var(--top-bar-button-border-color);
    border-radius: 4px;
    background-color: var(--top-bar-button-background);
    cursor: pointer;
    &:hover {
        filter: brightness(120%);
        border: 1px solid var(--top-bar-button-hover-border-color);
    }
    &:active {
        filter: brightness(80%);
    }
}
</style>
