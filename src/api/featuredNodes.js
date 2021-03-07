import { pick } from 'ramda'

export const fetchFeaturedNodes = async () => {
  const response = await fetch('/api/featured', {
    headers: {
      Accept: 'application/json',
    },
  })

  if (!response.ok) {
    throw new Error('Failed to fetch featured quizzes.')
  }

  const data = await response.json()

  return data.nodes.map((node) => ({
    ...pick(['id', 'ott', 'name', 'popularity', 'images', 'vernacular'], node),
    numSpecies: node.num_species,
  }))
}
