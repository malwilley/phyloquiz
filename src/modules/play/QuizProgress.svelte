<script>
  import Check from '../../components/icons/Check.svelte'
  import Times from '../../components/icons/Times.svelte'
  import { answers, numQuestions } from './store'
</script>

<div class="main">
  {#each $answers as answer, i}
    <div
      class="section"
      class:correct={answer?.data?.correct}
      class:incorrect={answer?.data?.correct === false}
    >
      {#if answer?.data?.correct}
        <div class="background" />
        <Check size={10} />
      {:else if answer?.data?.correct === false}
        <div class="background" />
        <Times size={10} />
      {/if}
    </div>
  {/each}
  {#each Array(numQuestions - $answers.length).fill(0) as _, i}
    <div class="section" />
  {/each}
</div>

<style type="text/scss">
  @import 'src/css/variables';
  @import 'src/css/media';

  .main {
    width: 100%;
    height: 12px;
    display: flex;
    border-radius: 8px;
    overflow: hidden;
    color: white;

    > * {
      flex: 1;
      background-color: $dark-20;

      &:not(:last-child) {
        margin-right: 4px;
      }
    }

    @include for-tablet-portrait-up {
      height: 16px;
    }
  }

  .section {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    border-radius: 4px;

    @for $i from 0 through 9 {
      &:nth-child(#{$i}) {
        z-index: #{10 - $i};
      }
    }

    .background {
      position: absolute;
      bottom: 0;
      left: 0;
      height: 100%;
      width: 100%;
      border-radius: 4px;
      animation: fill-elastic 1s;
    }

    :global(svg) {
      position: relative;
      stroke-width: 4;
    }
  }

  .correct {
    .background {
      background-color: $primary-60;
      box-shadow: inset 0 -2px darken($primary-60, 10%);
    }
  }

  .incorrect {
    .background {
      background-color: $error-300;
      box-shadow: inset 0 -2px darken($error-300, 10%);
    }
  }

  @keyframes fill-elastic {
    0% {
      width: 0;
    }

    16% {
      width: 132%;
    }

    28% {
      width: 87%;
    }

    44% {
      width: 105%;
    }

    59% {
      width: 98%;
    }

    73% {
      width: 101%;
    }

    88% {
      width: 100%;
    }

    100% {
      width: 100%;
    }
  }
</style>
