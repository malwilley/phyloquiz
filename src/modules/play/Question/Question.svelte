<script>
  import { actions, currentSelection } from '../store'
  import CenterContent from '../../../components/CenterContent.svelte'
  import SpeciesButton from './SpeciesButton.svelte'
  import CompareSpecies from './CompareSpecies.svelte'
  import InlineSpecies from '../InlineSpecies.svelte'
  import { fade } from 'svelte/transition'
  import isSmoothScrollingSupported from '../../../utils/isSmoothScrollingSupported'
  import { onMount } from 'svelte'

  export let leafData = {}

  let ref

  const { leafCompare, leaf1, leaf2 } = leafData

  onMount(() => {
    if (isSmoothScrollingSupported()) {
      window.scroll({ top: 0, behavior: 'smooth' })
    } else {
      window.scroll(0, 0)
    }
  })

  const scrollToQuestion = () => {
    if (ref && ref.scrollIntoView && isSmoothScrollingSupported()) {
      ref.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
    }
  }
</script>

<div
  class="question-container"
  bind:this={ref}
  in:fade={{ delay: 400 }}
  on:introend={scrollToQuestion}
>
  <CenterContent>
    <div class="question-text">
      Is <InlineSpecies leaf={leafCompare} image={false} />
      more closely related to
      <InlineSpecies leaf={leaf1} image={false} />
      or
      <InlineSpecies leaf={leaf2} image={false} />?
    </div>
    <CompareSpecies species={leafCompare} />
  </CenterContent>

  <div class="select-species-container">
    <SpeciesButton
      selected={leaf1 === $currentSelection}
      species={leaf1}
      on:click={() => actions.selectSpecies(leaf1)}
    />
    <SpeciesButton
      selected={leaf2 === $currentSelection}
      species={leaf2}
      on:click={() => actions.selectSpecies(leaf2)}
    />
  </div>
</div>

<style type="text/scss">
  @import 'src/css/variables';
  @import 'src/css/media';

  .question-container {
    padding-bottom: 6rem;
    overflow-x: hidden;
  }

  .question-text {
    margin: 2rem 0;
    text-align: center;
    font-size: 1.05rem;
    line-height: 1.5;

    @include for-tablet-portrait-up {
      margin: 3rem 0;
      font-size: 1.25rem;
    }
  }

  .select-species-container {
    display: flex;
    justify-content: space-around;
    align-items: center;
    flex-wrap: wrap;

    margin: 0 auto;
    max-width: 72rem;
    border-radius: 1rem;
  }
</style>
