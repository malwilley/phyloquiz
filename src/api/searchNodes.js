import { stringify } from 'querystringify'
import { httpGet } from './common'

export const searchNodes = async (query) => {
  const nodes = await httpGet(`/api/nodes${stringify({ q: query }, true)}`)

  return nodes
}
