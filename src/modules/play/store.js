import { writable, derived, get } from 'svelte/store'
import { all, dropLast, update, zipWith } from 'ramda'
import { fetchQuestion } from '../../api/questions'
import { fetchAnswer } from '../../api/answer'

export const numQuestions = 5

const notAsked = { type: 'notAsked' }
const fetching = { type: 'fetching' }
const emptySelections = Array(numQuestions).fill(null)

export const ott = writable(null)
export const quizInfo = writable(notAsked)
export const questions = writable([])
export const answers = writable(emptySelections)
export const selections = writable([])

export const questionIndex = derived(
  questions,
  ($questions) => $questions.length - 1,
)
export const questionNumber = derived(questionIndex, ($questionIndex) =>
  Math.max($questionIndex + 1, 1),
)
export const currentQuestion = derived(
  [questions, questionIndex],
  ([$questions, $questionIndex]) => $questions?.[$questionIndex] ?? notAsked,
)
export const currentSelection = derived(
  [selections, questionIndex],
  ([$selections, $questionIndex]) => $selections?.[$questionIndex] ?? null,
)
export const currentAnswer = derived(
  [answers, questionIndex],
  ([$answers, $questionIndex]) => $answers?.[$questionIndex] ?? notAsked,
)

export const score = derived(answers, ($answers) => {
  const val = $answers.reduce((score, answer) => {
    return score + (answer?.data?.correct ? 1 : 0)
  }, 0)

  return val
})

export const onLastQuestion = derived(
  questionIndex,
  ($questionIndex) => $questionIndex === numQuestions - 1,
)

export const allQuestionsCompleted = derived(answers, ($answers) =>
  all((answer) => answer?.type === 'success', $answers),
)

export const done = derived(
  [questionIndex, allQuestionsCompleted],
  ([$questionIndex, $allQuestionsCompleted]) =>
    $questionIndex >= numQuestions && $allQuestionsCompleted,
)

export const currentPageType = derived(
  [currentAnswer, done],
  ([$currentAnswer, $done]) => {
    if ($done) {
      return 'summary'
    }

    if ($currentAnswer?.type === 'success') {
      return 'answer'
    }

    return 'question'
  },
)

export const questionAnswerSummary = derived(
  [done, questions, answers],
  ([$done, $questions, $answers]) => {
    if (!$done) {
      return null
    }

    return zipWith(
      (questionUnion, answerUnion) => {
        const question = questionUnion.data
        const answer = answerUnion.data

        return { question, answer }
      },
      $questions,
      $answers,
    )
  },
)

export const actions = {
  startQuiz: async (incomingOtt) => {
    ott.set(incomingOtt)

    actions.playAgain()
  },

  selectSpecies: (leaf) => {
    const index = get(questionIndex)
    selections.update(($selections) => update(index, leaf, $selections))
  },

  generateQuestion: async () => {
    const quizOtt = get(ott)
    const index = get(questionIndex)
    questions.update(update(index, fetching))

    try {
      const questionResponse = await fetchQuestion(quizOtt)

      if (quizInfo.type !== 'success') {
        quizInfo.set({
          type: 'success',
          data: { title: questionResponse.quizTitle },
        })
      }

      questions.update(($questions) => [
        ...dropLast(1, $questions),
        { type: 'success', data: questionResponse },
      ])
    } catch (e) {
      console.error(e)
      questions.update(($questions) => [
        ...dropLast(1, $questions),
        { type: 'error', message: e.message },
      ])
    }
  },

  nextQuestion: async () => {
    questions.update(($questions) => [...$questions, fetching])

    await actions.generateQuestion()
  },

  checkAnswer: async () => {
    const question = get(currentQuestion)
    const selectedSpecies = get(currentSelection)
    const { leafCompare, leaf1, leaf2 } = question.data

    const answerIndex = get(questionIndex)
    answers.update(update(answerIndex, fetching))

    try {
      const {
        leaf1Ancestor,
        leaf2Ancestor,
        additionalCloseAncestors,
        additionalFarAncestors,
        correct,
      } = await fetchAnswer({
        leafCompareId: leafCompare.id,
        leaf1Id: leaf1.id,
        leaf2Id: leaf2.id,
        userChoice: selectedSpecies.id,
      })

      const pair1 = { leaf: leaf1, ancestor: leaf1Ancestor }
      const pair2 = { leaf: leaf2, ancestor: leaf2Ancestor }
      const selected = selectedSpecies.id === leaf1.id ? pair1 : pair2
      const unselected = selectedSpecies.id === leaf1.id ? pair2 : pair1

      const data = {
        correct,
        selected,
        unselected,
        additionalCloseAncestors,
        additionalFarAncestors,
      }

      answers.update(update(answerIndex, { type: 'success', data }))
    } catch (e) {
      console.error(e)
      answers.update(update(answerIndex, { type: 'error', message: e.message }))
    }
  },

  playAgain: () => {
    quizInfo.set(fetching)
    questions.set([])
    answers.set(emptySelections)
    selections.set(emptySelections)
    actions.nextQuestion()
  },
}
