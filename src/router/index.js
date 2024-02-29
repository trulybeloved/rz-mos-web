import { createRouter, createWebHistory } from 'vue-router'

import CharacterView from '../views/CharacterView.vue'
import WordsView from '../views/WordsView.vue'
import WikiView from '../views/WikiView.vue'

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
    },
    {
      path: '/wiki',
      name: 'wiki',
      component: WikiView
    }
  ]
})

export default router
