<script>
  import { numQuestions, score, questionAnswerSummary, quizOtt } from './store'
  import InlineSpecies from './InlineSpecies.svelte'
  import CenterContent from '../../components/CenterContent.svelte'
  import Check from '../../components/icons/Check.svelte'
  import Times from '../../components/icons/Times.svelte'
  import Play from '../../components/icons/Play.svelte'
  import { link } from 'svelte-routing'
</script>

<CenterContent>
  <div class="card score-card">
    <div class="score-text">Final score</div>
    <div class="score">
      <div class="numerator">{$score}</div>
      <div class="denominator">/{numQuestions}</div>
    </div>
    <a class="button play-again" href={`/generate/${$quizOtt}`}>
      <Play />
      <span>Play again?</span>
    </a>
    <a class="button secondary go-home" use:link href="/">
      Or find something new
    </a>
  </div>
  <h2>Your answers</h2>
  <ol>
    {#each $questionAnswerSummary as { leafCompare, leaf1, leaf2, selected, correct }, i}
      <li class="card question-answer">
        <h3>Question {i + 1}</h3>
        <div class="question">
          Is
          <InlineSpecies leaf={leafCompare} />
          more closely related to
          <InlineSpecies leaf={leaf1} />
          or
          <InlineSpecies leaf={leaf2} />
          ?
        </div>
        <div class="answer">
          <div class="answer-symbol" class:correct class:incorrect={!correct}>
            {#if correct}
              <span class="visually-hidden">You were correct.</span>
              <Check aria-hidden />
            {:else}
              <span class="visually-hidden">You were incorrect.</span>
              <Times aria-hidden />
            {/if}
          </div>
          You selected
          <InlineSpecies leaf={selected} />
        </div>
      </li>
    {/each}
  </ol>
</CenterContent>

<style type="text/scss">
  @import 'src/css/variables';
  @import 'src/css/media';

  .score-card {
    margin: 4rem auto;
    padding: 2rem;
    max-width: 400px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .score-text {
    @include text-style-caps;
    color: $text-color-light;
    margin-bottom: 1rem;
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
    margin: 2rem 0 1rem 0;
  }

  .question-answer {
    list-style: none;
    font-size: 1rem;
    line-height: 2;
    padding: 1rem;
    margin-bottom: 1rem;

    h3 {
      @include text-style-caps;
      color: $text-color-light;
      margin-bottom: 0.5rem;
    }

    @include for-tablet-portrait-up {
      font-size: 1.1rem;
      padding: 1rem 1.5rem;
    }
  }

  .answer {
    margin-top: 1rem;
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
