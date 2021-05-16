<script>
  import QuizProgress from './QuizProgress.svelte'
  import CenterContent from '../../components/CenterContent.svelte'
  import Times from '../../components/icons/Times.svelte'
  import { link } from 'svelte-routing'
  import { numQuestions, questionNumber, quizInfo, done } from './store'

  const title = $quizInfo?.data?.title ?? 'Unknown'
</script>

<div class="header">
  <a class="exit-link" aria-label="Exit quiz" href="/" use:link><Times /></a>
  <CenterContent>
    <div class="title">{title}</div>
    <div class="progress-text">
      {#if !$done}
        Question {$questionNumber} of {numQuestions}
      {:else}
        Review
      {/if}
    </div>
    <div class="progress-container">
      <QuizProgress />
    </div>
  </CenterContent>
</div>

<style type="text/scss">
  @import 'src/css/variables';
  @import 'src/css/media';

  .header {
    padding: 1rem 0 0.75rem 0;
    background-color: white;
    text-align: center;
    box-shadow: inset 0 0 0 1px $light-border-color;

    animation: pop-in-top 600ms ease-out;

    @include for-tablet-portrait-up {
      padding: 1.1rem 0 1rem 0;
    }
  }

  .exit-link {
    position: absolute;
    right: 0.4rem;
    top: 0.4rem;
    display: flex;
    align-items: center;
    justify-content: center;
    color: $text-color-light;
    height: 3rem;
    width: 3rem;
    border-radius: 50%;
    background-color: white;
    transition: color 200ms, box-shadow 200ms, background-color 200ms;

    &:hover,
    &:focus {
      color: $text-color-dark;
      background-color: $light-hover;
    }

    &:focus {
      box-shadow: 0 0 0 6px $primary-30;
    }

    &:active {
      background-color: $dark-10;
      box-shadow: 0 0 0 6px $primary-30;
    }

    :global(svg) {
      height: 1.5rem;
      width: 1.5rem;
    }

    @include for-tablet-portrait-up {
      right: 0.5rem;
      top: 0.5rem;
      height: 3.5rem;
      width: 3.5rem;

      :global(svg) {
        height: 1.9rem;
        width: 1.9rem;
      }
    }
  }

  .title {
    font-size: 1.4rem;
    font-weight: bold;
    text-transform: capitalize;
    margin-bottom: 0.6rem;

    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;

    @include for-tablet-portrait-up {
      font-size: 2rem;
    }
  }

  .progress-text {
    display: none;

    @include for-tablet-portrait-up {
      display: block;
      height: 1rem;
      margin-bottom: 8px;

      @include text-style-caps;
      color: $text-color-light;
    }
  }

  .progress-container {
    margin: 0 auto;
    max-width: 30rem;
  }

  @keyframes pop-in-top {
    from {
      transform: translateY(-100%);
    }

    to {
      transform: translateY(0);
    }
  }
</style>
