import { pick } from 'ramda'
import { httpGet } from './common'

export const fetchFeaturedNodes = async () => {
  const nodes = await httpGet('/api/featured_nodes')

  return nodes.map((node) => ({
    ...pick(['id', 'ott', 'name', 'popularity', 'images', 'vernacular'], node),
    numSpecies: node.num_species,
  }))
}
