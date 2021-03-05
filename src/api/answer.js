export const fetchAnswer = async ({
  leafCompareId,
  leaf1Id,
  leaf2Id,
  userChoice,
}) => {
  const response = await fetch('/api/check_answer', {
    method: 'POST',
    body: JSON.stringify({
      leaf_compare_id: leafCompareId,
      leaf_1_id: leaf1Id,
      leaf_2_id: leaf2Id,
      user_choice: userChoice,
    }),
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
  })

  if (!response.ok) {
    throw new Error('Error checking answer.')
  }

  const result = await response.json()

  return {
    leaf1Ancestor: result.leaf_1_ancestor,
    leaf2Ancestor: result.leaf_2_ancestor,
    additionalCloseAncestors: result.close_ancestors,
    additionalFarAncestors: result.far_ancestors,
    correct: result.correct,
  }
}
