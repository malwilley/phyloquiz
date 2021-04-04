<script>
  import Check from '../../../components/icons/Check.svelte'
  import { createEventDispatcher } from 'svelte'
  import getVernacularOrName from '../../../utils/getVernacularOrName'
  import QuestionSpeciesLabel from './QuestionSpeciesLabel.svelte'

  export let species
  export let selected

  const dispatch = createEventDispatcher()
  const name = getVernacularOrName(species)
</script>

<button
  class="main"
  class:main--selected={selected}
  on:click={() => dispatch('click')}
>
  <img class="background-image" alt="" src={species.thumbnail} />
  <img
    class="foreground-image"
    alt={`Image of ${name}`}
    src={species.thumbnail}
  />
  <div class="name">
    <QuestionSpeciesLabel leaf={species} />
  </div>
  <div class="selected-stamp" aria-hidden>
    <Check />
  </div>
</button>

<style type="text/scss">
  @import 'src/css/variables';
  @import 'src/css/media';

  .main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
    height: 17rem;
    border-radius: 0;

    flex: 1 0;

    padding-bottom: 4rem;

    // This transform is necessary to prevent Chrome from causing
    transform: translate(0);

    &:hover:not(.main--selected):not(:active),
    &:focus:not(.main--selected):not(:active) {
      .foreground-image {
        box-shadow: 0 0 0 0.4rem rgba($primary-60, 0.5);
      }
    }

    &:active {
      .foreground-image {
        box-shadow: 0 0 0 0.75rem rgba($primary-60, 0.5);
      }
    }

    &--selected {
      .selected-stamp {
        display: flex;
        box-shadow: $box-shadow-small;

        :global(svg) {
          height: 1.5rem;
          width: 1.5rem;
          stroke-width: 3;
        }
      }
    }

    @include for-tablet-portrait-up {
      overflow: hidden;
      height: 20rem;
      padding-bottom: 3rem;

      box-shadow: 0 1rem 1rem -1rem rgba($dark-600, 0.05),
        0 1.5rem 1.5rem 0 rgba($dark-600, 0.05);
      border-radius: 1rem;

      &:first-child {
        margin-right: 2rem;
      }
    }
  }

  .background-image {
    display: none;

    @include for-tablet-portrait-up {
      display: block;
      position: absolute;
      left: 0;
      top: 50%;
      filter: $bg-image-filter;
      width: 100%;
      transform: translateY(-50%);
      pointer-events: none;
    }
  }

  .foreground-image {
    background-color: $dark-20;
    height: 150px;
    width: 150px;
    position: relative;
    border-radius: 1rem;
    pointer-events: none;
    transition: box-shadow 150ms;
    box-shadow: 0 1rem 2rem rgba($dark-600, 0.15),
      0 0.2rem 0.5rem rgba($dark-600, 0.1), 0 0 0 1px rgba($dark-600, 0.05);

    @include for-tablet-portrait-up {
      box-shadow: 0 0.25rem 0.25rem 0.1rem rgba($dark-600, 0.15),
        0 0.25rem 0.5rem 0.25rem rgba($dark-600, 0.1);
    }
  }

  .selected-stamp {
    display: none;

    position: absolute;
    justify-content: center;
    align-items: center;
    top: 1rem;
    right: 1rem;
    width: 3rem;
    height: 3rem;
    border-radius: 1.5rem;
    background-color: $primary-60;
    border: 4px solid white;
    color: white;
    animation: puff-in-center 200ms ease-out;
  }

  .name {
    position: absolute;
    bottom: 0.5rem;
    left: 0.5rem;
    width: calc(100% - 1rem);

    background-color: white;

    display: flex;
    justify-content: center;
    align-items: center;

    font-weight: bold;
    text-align: center;
    text-transform: capitalize;
    min-height: 3.5rem;
    border-radius: 0.5rem;
    padding: 0.5rem;
    color: $text-color-dark;

    font-family: $serif-font;

    box-shadow: inset 0 0 0 1px $dark-20,
      0 1rem 1rem -1rem rgba($dark-600, 0.05),
      0 1.5rem 1.5rem 0 rgba($dark-600, 0.05);
    font-size: 0.9rem;

    @include for-tablet-portrait-up {
      bottom: 0;
      left: 0;
      width: 100%;
      background-color: white;
      box-shadow: none;
      font-size: 1.25rem;
      border-radius: 0;
      padding: 0.5rem 2rem;
      min-height: 3rem;
    }
  }

  @keyframes puff-in-center {
    0% {
      transform: translateZ(0) scale(2);
      opacity: 0;
    }
    100% {
      transform: translateZ(0) scale(1);
      opacity: 1;
    }
  }
</style>
