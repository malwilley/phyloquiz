import { writable, get } from 'svelte/store'
import { fetchFeaturedNodes } from '../../api/featuredNodes'
import { searchNodes } from '../../api/searchNodes'
import { isEmpty } from 'ramda'

const notAsked = { type: 'notAsked' }
const fetching = { type: 'fetching' }

export const featuredNodes = writable(notAsked)
export const searchedNodes = writable(notAsked)

export const actions = {
  fetchFeatured: async () => {
    try {
      if (get(featuredNodes)?.type === 'success') {
        return
      }

      featuredNodes.set(fetching)
      const nodes = await fetchFeaturedNodes()
      featuredNodes.set({ type: 'success', data: nodes })
    } catch (e) {
      console.error(e)
      featuredNodes.set({ type: 'error', message: e.message })
    }
  },

  searchNodes: async (query) => {
    try {
      if (isEmpty(query) || searchedNodes?.query === query) {
        return
      }

      searchedNodes.set({
        type: 'fetching',
        query,
      })
      const nodes = await searchNodes(query)
      searchedNodes.set({ type: 'success', data: nodes, query })
    } catch (e) {
      console.error(e)
      featuredNodes.set({ type: 'error', message: e.message })
    }
  },

  clearSearchedNodes: () => {
    searchedNodes.set(notAsked)
  },
}
