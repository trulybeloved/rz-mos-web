import { ref, onUnmounted } from 'vue'
import Mark from 'mark.js'

export function useHighlight(options = {}) {
    const markInstance = ref(null)
    const isHighlighting = ref(false)

    const initializeMarker = (element) => {
        if (element) {
            markInstance.value = new Mark(element)
        }
    }

    const highlight = (term, customOptions = {}) => {
        if (!markInstance.value || !term) return

        isHighlighting.value = true

        // Clear previous highlights
        markInstance.value.unmark()

        // Default options
        const defaultOptions = {
            accuracy: 'partially',
            // ignorePunctuation: ':;.,-–—‒_(){}[]!\'"+=',
            className: 'highlighted-text',
            each: (element) => {
                element.setAttribute('data-highlighted', 'true')
            },
            done: () => {
                isHighlighting.value = false
            },
            ...options,
            ...customOptions
        }

        markInstance.value.mark(term, defaultOptions)
    }

    const unmark = () => {
        if (markInstance.value) {
            markInstance.value.unmark()
        }
        isHighlighting.value = false
    }

    const highlightRegex = (regex, customOptions = {}) => {
        if (!markInstance.value) return

        isHighlighting.value = true
        markInstance.value.unmark()

        const defaultOptions = {
            element: 'mark',
            className: 'regex-highlight',
            done: () => {
                isHighlighting.value = false
            },
            ...options,
            ...customOptions
        }

        markInstance.value.markRegExp(regex, defaultOptions)
    }

    // Cleanup on unmount
    onUnmounted(() => {
        unmark()
        markInstance.value = null
    })

    return {
        initializeMarker,
        highlight,
        unmark,
        highlightRegex,
        isHighlighting,
        markInstance
    }
}