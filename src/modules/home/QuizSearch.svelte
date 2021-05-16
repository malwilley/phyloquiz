<script>
  import { actions, searchedNodes } from './store'
  import debounce from 'debounce'
  import { clickOutside } from '../../directives/clickOutside'
  import getVernacularOrName from '../../utils/getVernacularOrName'
  import { navigate } from 'svelte-routing'
  import SpiralPhyloTree from '../../components/SpiralPhyloTree.svelte'
  import Search from '../../components/icons/Search.svelte'
  import { find, isEmpty } from 'ramda'

  let query = ''
  let lastSearchedQuery = query
  let highlightedIndex = 0
  let wrapperRef
  let inputRef

  let focused = false

  const resetHighlightedIndex = () => {
    highlightedIndex = 0
  }

  $: items = $searchedNodes?.data ?? []
  $: {
    if (items) {
      resetHighlightedIndex()
    }
  }
  $: isOpen = focused && $searchedNodes.type !== 'notAsked' && !isEmpty(query)
  $: {
    if (isEmpty(query)) {
      actions.clearSearchedNodes()
    }
  }

  const debouncedSearch = debounce((q) => {
    actions.searchNodes(q)
    lastSearchedQuery = q
  }, 300)

  const onInput = (e) => {
    const value = e.target.value

    if (value !== query) {
      debouncedSearch(value)
    }
  }

  const setFocus = (focus) => {
    focused = focus
  }

  const reset = () => {
    query = ''
  }
  const focus = () => setFocus(true)
  const unfocus = () => {
    setFocus(false)
    resetHighlightedIndex()
  }

  const selectItem = (item) => {
    query = item.vernacular
    navigate(`/generate/${item.ott}`)
  }

  const selectHighlightedItem = () => {
    if (highlightedIndex < 0) {
      return
    }

    const item = items[highlightedIndex]

    if (item) {
      selectItem(item)
    }
  }

  const setHighlightedIndex = (newIndex) => {
    if (!items.length) {
      return
    }

    if (newIndex < 0) {
      highlightedIndex = items.length - 1
      return
    }

    if (newIndex >= items.length) {
      highlightedIndex = 0
      return
    }

    highlightedIndex = newIndex
  }

  const onKeyDown = (e) => {
    switch (e.key) {
      case 'Escape': {
        e.preventDefault()
        reset()
        return
      }
      case 'Enter': {
        e.preventDefault()
        return selectHighlightedItem()
      }
      case 'ArrowUp': {
        e.preventDefault()
        return setHighlightedIndex(highlightedIndex - 1)
      }
      case 'ArrowDown': {
        e.preventDefault()
        return setHighlightedIndex(highlightedIndex + 1)
      }
      case 'Tab': {
        return unfocus()
      }
    }
  }
</script>

<div
  class="wrapper"
  bind:this={wrapperRef}
  use:clickOutside
  on:clickOutside={unfocus}
>
  <div class="decorative-tree" aria-hidden>
    <SpiralPhyloTree />
  </div>
  <div role="combobox" aria-expanded={isOpen} aria-owns="results">
    <input
      autocorrect="off"
      title="Search quizzes"
      type="text"
      on:keydown={onKeyDown}
      on:input={onInput}
      on:focus={focus}
      bind:this={inputRef}
      bind:value={query}
      aria-label="Search quizzes"
      aria-autocomplete="list"
      aria-controls="results"
      aria-activedescendant={items?.[highlightedIndex]?.ott}
      placeholder="Primates, orchids, parrots, etc..."
    />
    <div class="search-icon" aria-hidden>
      <Search size={18} />
    </div>
  </div>
  <ul class="flyout" class:hidden={!isOpen} id="results" role="listbox">
    {#if $searchedNodes.type === 'fetching'}
      {#each Array(5) as _}
        <li class="flyout-item skeleton" aria-hidden>
          <div>
            <div class="name skeleton" />
            <div class="num-species skeleton" />
          </div>
          <div class="images-container">
            {#each Array(5) as _}
              <div class="image" />
            {/each}
          </div>
        </li>
      {/each}
    {:else if $searchedNodes.type === 'success'}
      {#each $searchedNodes.data as node, i}
        <li
          class="flyout-item"
          class:highlighted={highlightedIndex === i}
          on:click={() => selectItem(node)}
          on:mouseenter={() => setHighlightedIndex(i)}
        >
          <div>
            <div class="name" role="option" id={node.ott}>
              {getVernacularOrName(node)}
              {#if node.name}<span> ({node.name})</span>{/if}
            </div>
            <div class="num-species">
              {node.num_species?.toLocaleString()}
              playable species
            </div>
          </div>
          <div class="images-container">
            {#each node.images as imageUrl, i}
              <img class="image" alt="" src={imageUrl} />
            {/each}
          </div>
        </li>
      {/each}
      {#if $searchedNodes.data.length === 0}
        <div class="flyout-item info ">
          <p>
            No playable quizzes found for <strong>"{lastSearchedQuery}"</strong>
          </p>
          <p class="note">
            Note: some groups do not have enough data for quiz generation.
          </p>
        </div>
      {/if}
    {:else if $searchedNodes.type === 'error'}
      <div class="flyout-item info ">
        <p>
          Failed to retrieve search results for <strong
            >"{lastSearchedQuery}"</strong
          >
        </p>
        <p class="note">
          {$searchedNodes.message}
        </p>
      </div>
    {/if}
  </ul>
</div>

<style lang="scss">
  @import 'src/css/variables';
  @import 'src/css/media';

  $default-shadow: $box-shadow-card;

  .wrapper {
    grid-area: search;
    position: relative;
    width: 100%;
    max-width: 30rem;
  }

  [role='combobox'] {
    position: relative;

    background: white;
    height: 3rem;
    line-height: 3rem;
    border-radius: 1.5rem;
    border: none;
    box-shadow: $default-shadow;
    color: $text-color-dark;
    transition: all 200ms ease-out;
    overflow: hidden;

    margin: 0 2rem;

    &:focus-within {
      box-shadow: $default-shadow, 0 0 0 0.5rem rgba($primary-60, 0.3);
    }

    @include for-tablet-portrait-up {
      height: 3.5rem;
      line-height: 3.5rem;
      border-radius: 1.75rem;
      margin: 0;
    }
  }

  .search-icon {
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 4rem;
    pointer-events: none;

    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
  }

  input {
    position: relative;
    width: 100%;
    background: white;
    height: 100%;
    padding: 0 2rem 0 3.5rem;
    border: none;
    line-height: 3rem;
    font-size: 1rem;

    @include for-phone-only {
      // Only decrease placeholder since we need font-size to be 1rem so mobile safari doesn't autozoom on focus
      &::placeholder {
        font-size: 0.8rem;
      }
    }

    @include for-tablet-portrait-up {
      line-height: 3.5rem;
    }
  }

  .flyout {
    position: absolute;
    top: calc(100% + 1rem);
    width: 100%;

    background: white;
    border-radius: 1rem;
    z-index: 10;

    overflow-y: auto;
    overflow-x: hidden;
    max-height: 30rem;

    box-shadow: 0 1rem 1rem -0.5rem rgba($dark-600, 0.15),
      0 1.5rem 1.5rem 0 rgba($dark-600, 0.1);

    &.hidden {
      display: none;
    }
  }

  .flyout-item {
    padding: 0.5rem 1rem;
    cursor: pointer;
    position: relative;

    display: flex;
    justify-content: space-between;
    align-items: center;
    min-height: 3.5rem;

    &:first-child {
      margin-top: 1rem;
    }

    &:last-child {
      margin-bottom: 1rem;
    }

    &.info {
      pointer-events: none;
      font-family: $sans-serif-font;
      font-size: 0.9rem;
      display: block;
      padding: 0.5rem 1.5rem;

      .note {
        font-size: 0.75rem;
        color: $text-color-light;
        margin-top: 0.5rem;
      }
    }

    &.highlighted {
      background-color: $light-hover;

      .name {
        text-decoration: underline;
      }
    }

    .name {
      font-size: 0.9rem;
      font-weight: bold;

      span {
        color: $text-color-light;
        font-weight: normal;
      }

      &.skeleton {
        width: 10rem;
        height: 0.9rem;
        margin-bottom: 0.1rem;
        background-color: $dark-20;
      }
    }

    .num-species {
      font-family: $sans-serif-font;
      font-size: 0.7rem;
      letter-spacing: 0.3px;
      color: $text-color-light;

      &.skeleton {
        width: 6rem;
        height: 0.7rem;
        margin-bottom: 0.1rem;
        background-color: $dark-10;
      }
    }

    .images-container {
      display: flex;
      flex-wrap: wrap;
      height: 2.2rem;
      overflow: hidden;
      padding-left: 1rem;
      justify-content: flex-end;
      max-width: 50%;
    }

    .image {
      height: 2.2rem;
      width: 2.2rem;
      border-radius: 1.1rem;
      box-sizing: border-box;
      border: 2px solid white;
      margin-left: -1rem;
      background-color: $dark-20;
    }
  }

  .decorative-tree {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    z-index: -1;
  }
</style>
