<script>
  import ThumbUp from '../../../components/icons/ThumbUp.svelte'
  import ThumbDown from '../../../components/icons/ThumbDown.svelte'
  import { questionNumber, quizUuid } from '../store'
  import { rateQuestion } from '../../../api/rateQuestion'
  import { actions } from '../../notification/store'
  import { fade } from 'svelte/transition'

  let rating = null
  let status = 'novote'

  const rate = async (isGood) => {
    const previousRating = rating
    rating = isGood
    status = 'posting'

    try {
      await rateQuestion({
        quizUuid: $quizUuid,
        questionNumber: $questionNumber,
        isGood,
      })

      status = 'voted'
    } catch {
      rating = previousRating
      status = 'novote'
      actions.pushNotification({
        message: 'Failed to rate question. Please try again.',
      })
    }
  }
</script>

<div class="rate-question">
  <div>
    {#if rating === null}
      <div out:fade>
        Was this a <strong>good question</strong>?
      </div>
    {:else}
      <div in:fade={{ delay: 400 }}>Thanks for the input!</div>
    {/if}
  </div>
  <div class="thumbs-container">
    <button
      class="thumb-button up"
      class:selected={rating === true}
      disabled={status === 'posting'}
      on:click={() => rate(true)}
    >
      <ThumbUp />
      <div class="visually-hidden">Vote good question</div>
    </button>
    <button
      class="thumb-button down"
      class:selected={rating === false}
      disabled={status === 'posting'}
      on:click={() => rate(false)}
    >
      <ThumbDown />
      <div class="visually-hidden">Vote bad question</div>
    </button>
  </div>
</div>

<style lang="scss">
  @import 'src/css/variables';

  .rate-question {
    position: relative;
    display: flex;
    justify-content: space-between;
    height: 4rem;
    padding: 0 1rem 0 2rem;
    border-radius: 0.5rem;

    margin: 1.5rem auto 0 auto;
    max-width: 22rem;

    font-family: $sans-serif-font;
    font-size: $sans-serif-size-medium;
    line-height: 4rem;

    box-shadow: $box-shadow-card;
    background: white;

    overflow: visible;

    &::after {
      content: '';
      position: absolute;
      top: -12px;
      left: 50%;
      transform: translateX(-50%);

      border-width: 0 12px 12px;
      border-color: white transparent;
      border-style: solid;
    }
  }

  .thumbs-container {
    display: flex;
    align-items: center;
    flex-shrink: 0;
  }

  .thumb-button {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 2.5rem;
    width: 2.5rem;
    border-radius: 0.25rem;

    color: $dark-600;

    &.up {
      color: $correct-color;

      &.selected {
        background-color: rgba($correct-color, 0.1);
      }

      &:hover:not(:active):not(.selected) {
        :global(svg) {
          transform: translateY(-2px);
        }
      }

      &:focus {
        border: 3px solid $correct-color;

        &:not(:focus-visible) {
          border: none;
        }
      }

      &:active:not(.selected) {
        :global(svg) {
          transform: translateY(1px);
        }
      }
    }
    &.down {
      color: $incorrect-color;

      &.selected {
        background-color: rgba($incorrect-color, 0.1);
      }

      &:hover:not(:active):not(.selected) {
        :global(svg) {
          transform: translateY(2px);
        }
      }

      &:focus {
        border: 3px solid $incorrect-color;

        &:not(:focus-visible) {
          border: none;
        }
      }

      &:active:not(.selected) {
        :global(svg) {
          transform: translateY(-1px);
        }
      }
    }

    &:active:not(.selected) {
      background: $dark-10;
    }

    &:hover {
      background: $light-hover;
    }

    &:not(:last-child) {
      margin-right: 0.5rem;
    }

    :global(svg) {
      height: 1.25rem;
      width: 1.25rem;
      transition: 200ms transform;
    }
  }
</style>
