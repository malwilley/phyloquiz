export const searchNodes = async (query) => {
  const response = await fetch('/api/search_nodes', {
    method: 'POST',
    body: JSON.stringify({
      query,
    }),
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
  })
  if (!response.ok) {
    throw new Error('')
  }

  const data = await response.json()

  return data
}
