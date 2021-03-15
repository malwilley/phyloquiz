import { httpGet } from './common'

export const getQuiz = async (quizUuid) => {
  const quizResponse = await httpGet(`/api/quiz/${quizUuid}`)

  return {
    quiz: quizResponse.quiz,
    nextQuestion: quizResponse.next_question,
    completedQuestions: quizResponse.completed_questions,
  }
}
