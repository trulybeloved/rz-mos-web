import { defineStore } from 'pinia'

export const useGeneralStore = defineStore('general', {
    state: () => ({ useDarkMode: true }),

    getters: {
        getDarkMode: (state) => {
            return state.useDarkMode
        },
    },

    actions: {
        toggleDarkMode() {
            this.useDarkMode = !this.useDarkMode
        },
        setDarkMode(option) {
            this.useDarkMode = option
        }
    },
})