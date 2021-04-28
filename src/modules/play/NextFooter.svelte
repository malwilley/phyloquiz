<script>
  import {
    actions,
    currentPageType,
    currentSelection,
    currentAnswer,
    allQuestionsCompleted,
  } from './store'
  import { isNil } from 'ramda'
  import SimpleLoader from '../../components/SimpleLoader.svelte'
  import Arrow from '../../components/icons/Arrow.svelte'

  const getFooterProps = (
    pageType,
    selectedSpecies,
    currentAnswer,
    allQuestionsCompleted,
  ) => {
    switch (pageType) {
      case 'answer':
        return {
          show: true,
          label: allQuestionsCompleted ? 'Review' : 'Next question',
          action: () => actions.nextQuestion(),
        }
      case 'question':
        return {
          show: !isNil(selectedSpecies),
          label: 'Check answer',
          status: currentAnswer.type,
          action: () => actions.submitAnswer(),
        }
      case 'summary':
      default:
        return { show: false, label: 'Review' }
    }
  }

  $: props = getFooterProps(
    $currentPageType,
    $currentSelection,
    $currentAnswer,
    $allQuestionsCompleted,
  )
</script>

<div class="next-footer" class:next-footer--hidden={!props.show}>
  <div class="center-content button-container">
    <button
      class="button"
      on:click={props.action}
      disabled={!props.show || props.status === 'fetching'}
    >
      <span>{props.label}</span>
      {#if props.status === 'fetching'}
        <SimpleLoader />
      {:else}
        <Arrow direction="right" />
      {/if}
    </button>
  </div>
</div>

<style type="text/scss">
  @import 'src/css/variables';
  @import 'src/css/media';

  .next-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: white;
    height: 5.5rem;
    border-top: 1px solid $light-border-color;
    box-shadow: 0 -0.5rem 0.5rem 0 rgba($dark-600, 0.05);
    z-index: $z-index-next-footer;

    transform: translateY(0);

    transition: transform 300ms ease-out, box-shadow 300ms ease-out;

    &--hidden {
      transform: translateY(100%);
      box-shadow: none;
    }

    @include for-tablet-landscape-up {
      height: 6rem;
    }
  }

  .button-container {
    height: 100%;
    display: flex;
    justify-content: flex-end;
    align-items: center;
  }

  button {
    width: 100%;

    @include for-tablet-portrait-up {
      width: auto;
    }
  }
</style>
