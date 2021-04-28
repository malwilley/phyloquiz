import { writable, derived, get } from 'svelte/store'
import { all, range, update, zipWith } from 'ramda'
import { getQuiz } from '../../api/getQuiz'
import { getNextQuestion } from '../../api/getNextQuestion'
import { submitAnswer } from '../../api/submitAnswer'
import { actions as notificationActions } from '../notification/store'

export const numQuestions = 5

const notAsked = { type: 'notAsked' }
const fetching = { type: 'fetching' }
const emptySelections = Array(numQuestions).fill(null)

export const quizInfo = writable(notAsked)
export const questions = writable([])
export const answers = writable(emptySelections)
export const selections = writable([])
export const renderedPageType = writable('question')

export const quizOtt = derived(quizInfo, ($quizInfo) =>
  $quizInfo.type === 'success' ? $quizInfo.data.ott : null,
)
export const quizUuid = derived(quizInfo, ($quizInfo) =>
  $quizInfo.type === 'success' ? $quizInfo.data.uuid : null,
)
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

        return {
          ...question,
          correct: answer.correct,
          selected:
            answer.selected === question.leaf1.ott
              ? question.leaf1
              : question.leaf2,
        }
      },
      $questions,
      $answers,
    )
  },
)

const getCurrentPageTypeFromState = () => {
  if (get(done)) {
    return 'summary'
  }

  if (get(currentAnswer)?.type === 'success') {
    return 'answer'
  }

  return 'question'
}

const nextPage = () => {
  renderedPageType.set(null)
}

export const actions = {
  getQuiz: async (uuid) => {
    if (uuid === get(quizUuid)) {
      return
    }

    // Reset state
    quizInfo.set(fetching)
    questions.set([])
    answers.set(emptySelections)
    selections.set(emptySelections)
    renderedPageType.set('question')

    try {
      const { quiz, nextQuestion, completedQuestions } = await getQuiz(uuid)

      quizInfo.set({
        type: 'success',
        data: {
          title: quiz.vernacular || quiz.name,
          uuid: quiz.uuid,
          ott: quiz.ott,
        },
      })

      questions.set([
        ...completedQuestions.map((question) => ({
          type: 'success',
          data: {
            leafCompare: question.compare,
            leaf1: question.option1,
            leaf2: question.option2,
          },
        })),
        ...(nextQuestion
          ? [
              {
                type: 'success',
                data: {
                  leafCompare: nextQuestion.compare,
                  leaf1: nextQuestion.option1,
                  leaf2: nextQuestion.option2,
                },
              },
            ]
          : [notAsked]), // make this more explicit
      ])
      answers.set([
        ...completedQuestions.map(({ correct, selected }) => ({
          type: 'success',
          data: { correct, selected },
        })),
        ...range(0, numQuestions - completedQuestions.length).map(() => null),
      ])

      renderedPageType.set(getCurrentPageTypeFromState())
    } catch (e) {
      console.error(e)
      quizInfo.set({
        type: 'error',
        message: 'Something went wrong while retrieving your quiz.',
      })
    }
  },

  nextQuestion: async () => {
    const uuid = get(quizUuid)
    questions.update(($questions) => [...$questions, fetching])
    const index = get(questionIndex)

    if (get(allQuestionsCompleted)) {
      nextPage()
      return
    }

    try {
      const question = await getNextQuestion(uuid)

      if (question) {
        questions.update(($questions) =>
          update(index, { type: 'success', data: question }, $questions),
        )
      }

      nextPage()
    } catch (e) {
      console.error(e)
      questions.update(($questions) =>
        update(index, { type: 'error', message: e.message }, $questions),
      )
    }
  },

  submitAnswer: async () => {
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
      } = await submitAnswer({
        quizUuid: get(quizUuid),
        questionNumber: get(questionNumber),
        selectedOtt: selectedSpecies.ott,
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

      nextPage()
    } catch (e) {
      console.error(e)
      answers.update(update(answerIndex, { type: 'error', message: e.message }))
      notificationActions.pushNotification({
        message: 'Something went wrong. Please try again.',
      })
    }
  },

  startQuiz: async (incomingOtt) => {
    ott.set(incomingOtt)

    actions.playAgain()
  },

  selectSpecies: (leaf) => {
    const index = get(questionIndex)
    selections.update(($selections) => update(index, leaf, $selections))
  },

  playAgain: () => {
    quizInfo.set(fetching)
    questions.set([])
    answers.set(emptySelections)
    selections.set(emptySelections)
    actions.nextQuestion()
  },

  pageAnimationCompleted: () => {
    renderedPageType.set(getCurrentPageTypeFromState())
  },
}
