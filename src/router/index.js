import { createRouter, createWebHistory } from 'vue-router'

import CharacterView from '../views/CharacterView.vue'
import WordsView from '../views/WordsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: CharacterView
    },
    {
      path: '/words',
      name: 'words',
      component: WordsView
    }
  ]
})

export default router
