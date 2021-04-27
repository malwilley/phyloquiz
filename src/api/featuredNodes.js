import { pick } from 'ramda'
import { httpGet } from './common'

export const fetchFeaturedNodes = async () => {
  const nodes = await httpGet('/api/nodes/featured')

  return nodes.map((node) => ({
    ...pick(['id', 'ott', 'name', 'popularity', 'images', 'vernacular'], node),
    numSpecies: node.num_species,
  }))
}
