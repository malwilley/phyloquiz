import { httpPost } from './common'

export const rateQuestion = async ({ quizUuid, questionNumber, isGood }) => {
  await httpPost(
    `/api/quiz/${quizUuid}/questions/${questionNumber}/rate_question`,
    {
      is_good: isGood,
    },
  )
}
