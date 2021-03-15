import { httpPost } from './common'

export const generateQuiz = async (ott) => {
  const quiz = await httpPost('/api/generate_quiz', { ott })

  return quiz.uuid
}
