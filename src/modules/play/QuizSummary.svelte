<script>
  import { actions, numQuestions, score, questionAnswerSummary } from './store'
  import InlineSpecies from './InlineSpecies.svelte'
  import { onMount } from 'svelte'
  import CenterContent from '../../components/CenterContent.svelte'
  import Check from '../../components/icons/Check.svelte'
  import Times from '../../components/icons/Times.svelte'
  import Play from '../../components/icons/Play.svelte'
  import { link } from 'svelte-routing'
  import isSmoothScrollingSupported from '../../utils/isSmoothScrollingSupported'

  onMount(() => {
    if (isSmoothScrollingSupported()) {
      window.scroll({ top: 0, behavior: 'smooth' })
    } else {
      window.scroll(0, 0)
    }
  })
</script>

<CenterContent>
  <div class="top">
    <div class="score-text">Final score</div>
    <div class="score">
      <div class="numerator">{$score}</div>
      <div class="denominator">/{numQuestions}</div>
    </div>
    <button class="button play-again" on:click={() => actions.playAgain()}
      ><Play /><span>Play again?</span></button
    >
    <a class="button secondary go-home" use:link href="/"
      >Or find something new</a
    >
  </div>
  <h2>Your answers</h2>
  <ol>
    {#each $questionAnswerSummary as { question, answer }, i}
      <li class="question-answer">
        <h3>Question {i + 1}</h3>
        <div class="question">
          Is
          <InlineSpecies leaf={question.leafCompare} />
          more closely related to
          <InlineSpecies leaf={question.leaf1} />
          or
          <InlineSpecies leaf={question.leaf2} />
          ?
        </div>
        <div class="answer">
          <div
            class="answer-symbol"
            class:correct={answer.correct}
            class:incorrect={!answer.correct}
          >
            {#if answer.correct}
              <span class="visually-hidden">You were correct.</span>
              <Check aria-hidden />
            {:else}
              <span class="visually-hidden">You were incorrect.</span>
              <Times aria-hidden />
            {/if}
          </div>
          You selected
          <InlineSpecies leaf={answer.selected.leaf} />
        </div>
      </li>
    {/each}
  </ol>
</CenterContent>

<style type="text/scss">
  @import 'src/css/variables';
  @import 'src/css/media';

  .top {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 8rem 0;
    text-align: center;
  }

  .score-text {
    @include text-style-caps;
    color: $text-color-light;
  }

  .score {
    display: flex;
    align-items: flex-end;

    font-weight: bold;
    margin-bottom: 4rem;
    font-family: $sans-serif-font;

    line-height: 1;

    .numerator {
      font-size: 10rem;
    }

    .denominator {
      font-size: 2rem;
      color: $text-color-light;
      padding-bottom: 1rem;
    }
  }

  .play-again {
    width: 100%;
    height: 4rem;
    border-radius: 2rem;
    font-size: 1.25rem;

    @include for-tablet-portrait-up {
      width: 15rem;
    }
  }

  .go-home {
    margin-top: 1.5rem;
  }

  h2 {
    font-size: 2rem;
    font-weight: bold;
    margin-top: 2rem;
  }

  .question-answer {
    list-style: none;
    font-size: 1rem;
    line-height: 2;

    h3 {
      @include text-style-caps;
      margin: 2rem 0 0.75rem 0;
      color: $text-color-light;
    }

    @include for-tablet-portrait-up {
      font-size: 1.1rem;
    }
  }

  .answer {
    margin: 1rem 0 0 2rem;

    @include for-tablet-portrait-up {
      margin: 1rem 0 0 4rem;
    }
  }

  .answer-symbol {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    vertical-align: middle;
    height: 1.5rem;
    width: 1.5rem;
    border-radius: 50%;
    margin-right: 1rem;
    color: white;

    :global(svg) {
      height: 0.9rem;
      width: 0.9rem;
      stroke-width: 4;
    }

    &.correct {
      background-color: $correct-color;
    }

    &.incorrect {
      background-color: $incorrect-color;
    }
  }
</style>
