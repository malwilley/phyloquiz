export const httpGet = async (url) => {
  const response = await fetch(url, {
    headers: {
      Accept: 'application/json',
    },
  })

  if (!response.ok) {
    const resp = await response.json()
    throw new Error(resp?.description ?? 'Fetch error')
  }

  const result = await response.json()

  return result
}

export const httpPost = async (url, body) => {
  const response = await fetch(url, {
    method: 'POST',
    body: JSON.stringify(body),
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
  })

  if (!response.ok) {
    const resp = await response.json()
    throw new Error(resp?.description ?? 'Post error')
  }

  const result = await response.json()

  return result
}
