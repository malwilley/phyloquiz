<script>
  import InlineExternalLink from '../../../components/InlineExternalLink.svelte'
  import InlineSpecies from '../InlineSpecies.svelte'
  import printNodeAge from '../../../utils/printNodeAge'
  import getVernacularOrName from '../../../utils/getVernacularOrName'
  import { isEmpty } from 'ramda'

  export let leaf1
  export let leaf2
  export let leafFar
  export let node
  export let additionalNodes = []
</script>

<InlineSpecies leaf={leafFar} />
diverged from both
<InlineSpecies leaf={leaf1} />
and
<InlineSpecies leaf={leaf2} />
{#if node.age}
  at an earlier time point, around
  <strong> {printNodeAge(node.age)}.</strong>
{:else}at an earlier time point.{/if}

{#if !isEmpty(additionalNodes)}
  Groups encompassing all three species include
  {#each additionalNodes as additionalNode, i}
    <InlineExternalLink
      href={`https://www.onezoom.org/life/@=${additionalNode.ott}`}
    >
      {getVernacularOrName(additionalNode)}
      {#if additionalNode.vernacular}
        ({additionalNode.name})
      {/if}
    </InlineExternalLink>{#if i < additionalNodes.length - 2}<span>, </span>
    {:else if i === additionalNodes.length - 2}
      &nbsp;and
    {/if}
  {/each}.
{/if}
