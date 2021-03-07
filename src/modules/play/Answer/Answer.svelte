<script>
  import AnswerSpeciesCard from './AnswerSpeciesCard.svelte'
  import AnswerExplanationClose from './AnswerExplanationClose.svelte'
  import AnswerExplanationFar from './AnswerExplanationFar.svelte'
  import CenterContent from '../../../components/CenterContent.svelte'
  import { currentAnswer, currentQuestion } from '../store'
  import { onMount } from 'svelte'
  import isSmoothScrollingSupported from '../../../utils/isSmoothScrollingSupported'
  import InlineTreeViewer from './InlineTreeViewer.svelte'
  import isPhoneViewport from '../../../utils/isPhoneViewport'

  onMount(() => {
    if (isSmoothScrollingSupported()) {
      window.scroll({ top: 0, behavior: 'smooth' })
    } else {
      window.scroll(0, 0)
    }
  })

  const shouldShowSelectedFirst = isPhoneViewport()

  const {
    correct,
    selected,
    unselected,
    additionalCloseAncestors,
    additionalFarAncestors,
  } = $currentAnswer.data ?? {}
  const { leaf1, leaf2, leafCompare } = $currentQuestion?.data ?? {}

  const leaf1Props = {
    leaf: leaf1,
    correct: leaf1.id === selected.leaf.id ? correct : !correct,
    selected: leaf1.id === selected.leaf.id,
  }
  const leaf2Props = {
    leaf: leaf2,
    correct: !leaf1Props.correct,
    selected: !leaf1Props.selected,
  }

  const getCardProps = () => {
    const cardProps = [leaf1Props, leaf2Props]

    if (!shouldShowSelectedFirst || leaf1Props.selected) {
      return cardProps
    }

    return cardProps.reverse()
  }
</script>

<CenterContent>
  <div class="cards-container">
    <AnswerSpeciesCard {...getCardProps()[0]} />
    <AnswerSpeciesCard leaf={leafCompare} />
    <AnswerSpeciesCard {...getCardProps()[1]} />
  </div>

  {#if correct}
    <div class="correct">Correct!</div>
  {:else}
    <div class="incorrect">Incorrect.</div>
  {/if}

  <section>
    <p class="explain-section">
      {#if correct}
        <AnswerExplanationClose
          leaf1={selected.leaf}
          leaf2={leafCompare}
          node={selected.ancestor}
          additionalNodes={additionalCloseAncestors}
        />
      {:else}
        <AnswerExplanationClose
          leaf1={unselected.leaf}
          leaf2={leafCompare}
          node={unselected.ancestor}
          additionalNodes={additionalCloseAncestors}
        />
      {/if}
    </p>
    <p class="explain-section">
      {#if !correct}
        <AnswerExplanationFar
          leaf1={leafCompare}
          leaf2={unselected.leaf}
          leafFar={selected.leaf}
          node={selected.ancestor}
          additionalNodes={additionalFarAncestors}
        />
      {:else}
        <AnswerExplanationFar
          leaf1={leafCompare}
          leaf2={selected.leaf}
          leafFar={unselected.leaf}
          node={unselected.ancestor}
          additionalNodes={additionalFarAncestors}
        />
      {/if}
    </p>
  </section>
  <section>
    <InlineTreeViewer node={additionalFarAncestors[0]} />
  </section>
</CenterContent>

<style type="text/scss">
  @import 'src/css/variables';
  @import 'src/css/media';

  .correct,
  .incorrect {
    font-size: 2rem;
    font-weight: bold;
    margin-top: 2rem;

    @include for-tablet-landscape-up {
      margin-top: 4rem;
    }
  }

  .correct {
    color: $correct-color;
  }

  .incorrect {
    color: $incorrect-color;
  }

  .cards-container {
    display: grid;
    column-gap: 2rem;
    row-gap: 2rem;

    // Carousel on phones
    @include for-tablet-portrait-down {
      grid-template-columns: auto auto auto;
      margin: 0 -1rem; // expand to edge
      overflow-x: auto;
      scroll-snap-type: x proximity;
      scroll-behavior: smooth;
      padding: 1rem;
      scroll-padding: 1rem;
      white-space: nowrap;
      margin-top: 1rem;

      > :global(.card) {
        flex-shrink: 0;
        scroll-snap-align: start;
        width: 20rem;

        &:last-child {
          &::after {
            content: '';
            width: 1.25rem;
          }
        }
      }
    }

    @include for-tablet-landscape-up {
      grid-template-columns: 1fr 1fr 1fr;
      margin-top: 4rem;
    }
  }

  .explain-section {
    font-size: 1rem;
    line-height: 2;
    margin-top: 2rem;

    @include for-tablet-portrait-up {
      font-size: 1.1rem;
    }
  }
</style>
