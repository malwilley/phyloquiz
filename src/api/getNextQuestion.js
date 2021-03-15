import { httpGet } from './common'

export const getNextQuestion = async (quizUuid) => {
  const data = await httpGet(`/api/quiz/${quizUuid}/next_question`)

  return {
    leafCompare: data.compare,
    leaf1: data.option1,
    leaf2: data.option2,
  }
}
