<script>
  import { isNil } from 'ramda'

  import getVernacularOrName from '../../utils/getVernacularOrName'

  export let leaf
  export let image = true

  const name = getVernacularOrName(leaf)
</script>

<span class="inline-species" class:scientific={isNil(leaf.vernacular)}>
  {#if image}
    <img alt={`Image of ${name}`} src={leaf.thumbnail} />
    <span>{name}</span>
  {:else}
    {name}
  {/if}
</span>

<style type="text/scss">
  @import 'src/css/variables';

  .inline-species {
    align-items: center;
    font-weight: bold;
    text-transform: capitalize;

    &.scientific {
      font-style: italic;
      text-transform: none;
    }
  }

  img {
    vertical-align: middle;
    height: 2em;
    width: 2em;
    border-radius: 50%;

    border: 2px solid white;
    box-shadow: $box-shadow-small;

    margin: 2px 4px 2px 2px;
  }
</style>
