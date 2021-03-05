<script>
  import Question from './Question/Question.svelte'
  import Answer from './Answer/Answer.svelte'
  import QuizSummary from './QuizSummary.svelte'
  import { quizInfo, currentQuestion, currentPageType, actions } from './store'
  import MapHttpUnion from '../../components/MapHttpUnion.svelte'
  import { fade, fly } from 'svelte/transition'
  import PhyloLoader from '../../components/PhyloLoader.svelte'
  import NextFooter from './NextFooter.svelte'
  import PlayHeader from './PlayHeader.svelte'
  import { onMount } from 'svelte'

  export let ott

  onMount(() => {
    window.scrollTo(0, 0)

    if (ott) {
      actions.startQuiz(ott)
    }
  })
</script>

<div class="play-container">
  <MapHttpUnion value={$quizInfo}>
    <div slot="success">
      <PlayHeader />
      <div class="play-area" in:fade={{ delay: 400 }}>
        {#if $currentPageType === 'question'}
          <div out:fly|local={{ x: -500 }}>
            <MapHttpUnion value={$currentQuestion}>
              <div
                slot="fetching"
                class="loading"
                in:fade={{ delay: 400 }}
                out:fade
              >
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
                  <button class="button" on:click={actions.generateQuestion}
                    >Click to try again</button
                  >
                </div>
              </div>
            </MapHttpUnion>
          </div>
        {:else if $currentPageType === 'answer'}
          <div
            in:fly|local={{ x: 500, delay: 400 }}
            out:fly|local={{ x: -500 }}
          >
            <Answer />
          </div>
        {:else if $currentPageType === 'summary'}
          <div
            in:fly|local={{ x: 500, delay: 400 }}
            out:fly|local={{ x: -500 }}
          >
            <QuizSummary />
          </div>
        {/if}
        <NextFooter />
      </div>
    </div>
    <div slot="fetching" class="loading" out:fade>
      <PhyloLoader>Generating quiz...</PhyloLoader>
    </div>
  </MapHttpUnion>
</div>

<style type="text/scss">
  @import 'src/css/variables';

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
    position: absolute;
    left: 0;
    top: 50%;
    width: 100%;
    transform: translateY(-50%);
  }
</style>
