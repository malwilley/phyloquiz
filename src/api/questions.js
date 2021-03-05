export const fetchQuestion = async (ott) => {
  const response = await fetch('/api/generate', {
    method: 'POST',
    body: JSON.stringify({ ott }),
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
  })

  if (!response.ok) {
    throw new Error('')
  }

  const data = await response.json()

  return {
    quizTitle: data.quiz_title,
    leafCompare: data.leaf_compare,
    leaf1: data.leaf_1,
    leaf2: data.leaf_2,
  }
}
