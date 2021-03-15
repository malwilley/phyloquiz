import { httpPost } from './common'

export const submitAnswer = async ({
  quizUuid,
  selectedOtt,
  questionNumber,
}) => {
  const result = await httpPost(`/api/quiz/${quizUuid}/submit_answer`, {
    selected_ott: selectedOtt,
    question_number: questionNumber,
    quiz_uuid: quizUuid,
  })

  return {
    leaf1Ancestor: result.leaf_1_ancestor,
    leaf2Ancestor: result.leaf_2_ancestor,
    additionalCloseAncestors: result.close_ancestors,
    additionalFarAncestors: result.far_ancestors,
    correct: result.correct,
  }
}
