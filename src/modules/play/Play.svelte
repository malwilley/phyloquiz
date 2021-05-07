<script>
  import Question from './Question/Question.svelte'
  import Answer from './Answer/Answer.svelte'
  import QuizSummary from './QuizSummary.svelte'
  import { quizInfo, currentQuestion, renderedPageType, actions } from './store'
  import MapHttpUnion from '../../components/MapHttpUnion.svelte'
  import { fade, fly } from 'svelte/transition'
  import PhyloLoader from '../../components/PhyloLoader.svelte'
  import NextFooter from './NextFooter.svelte'
  import PlayHeader from './PlayHeader.svelte'
  import { onMount } from 'svelte'

  export let uuid

  onMount(() => {
    window.scrollTo(0, 0)

    if (uuid) {
      actions.getQuiz(uuid)
    }
  })
</script>

<div class="play-container">
  <MapHttpUnion value={$quizInfo}>
    <div slot="success">
      <PlayHeader />
      <div class="play-area" in:fade>
        {#if $renderedPageType === 'question'}
          <div
            class="animated-container"
            out:fly|local={{ x: -500 }}
            on:outroend={actions.pageAnimationCompleted}
          >
            <MapHttpUnion value={$currentQuestion}>
              <div slot="fetching" class="loading-question" out:fade>
                <PhyloLoader />
              </div>
              <div slot="success">
                <Question leafData={$currentQuestion?.data} />
              </div>
              <div class="center-content" slot="error">
                <div class="error-content">
                  <p class="error">
                    Something went wrong while generating your question.
                  </p>
                  <button class="button" on:click={() => actions.nextQuestion()}
                    >Click to try again</button
                  >
                </div>
              </div>
            </MapHttpUnion>
          </div>
        {:else if $renderedPageType === 'answer'}
          <div
            class="animated-container"
            in:fly|local={{ x: 500 }}
            out:fly|local={{ x: -500 }}
            on:outroend={actions.pageAnimationCompleted}
          >
            <Answer />
          </div>
        {:else if $renderedPageType === 'summary'}
          <div
            class="animated-container"
            in:fly|local={{ x: 500 }}
            out:fly|local={{ x: -500 }}
            on:outroend={actions.pageAnimationCompleted}
          >
            <QuizSummary />
          </div>
        {/if}
        <NextFooter />
      </div>
    </div>
    <div class="loading" slot="fetching" out:fade>
      <PhyloLoader>Retrieving quiz...</PhyloLoader>
    </div>
    <div class="center-content" slot="error">
      <div class="error-content">
        <p class="error">Something went wrong while retrieving your quiz.</p>
        <button class="button" on:click={() => actions.getQuiz(uuid)}
          >Click to try again</button
        >
      </div>
    </div>
  </MapHttpUnion>
</div>

<style type="text/scss">
  @import 'src/css/variables';

  .animated-container {
    will-change: opacity, transform;
  }

  .play-container {
    overflow-x: hidden;
  }

  .play-area {
    padding-bottom: 8rem;
  }

  .error-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-top: 8rem;
  }

  .error {
    font-weight: bold;
    font-family: $sans-serif-font;
    margin-bottom: 2rem;
    line-height: 2;
  }

  .loading {
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
  }

  .loading-question {
    height: 10rem;
    margin-top: 10rem;
  }
</style>
