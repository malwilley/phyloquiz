<script>
  import InlineExternalLink from '../../../components/InlineExternalLink.svelte'
  import InlineSpecies from '../InlineSpecies.svelte'
  import printNodeAge from '../../../utils/printNodeAge'
  import { isEmpty } from 'ramda'
  import getVernacularOrName from '../../../utils/getVernacularOrName'

  export let leaf1
  export let leaf2
  export let node
  export let additionalNodes = []
</script>

<InlineSpecies leaf={leaf1} />
and
<InlineSpecies leaf={leaf2} />
{#if node.age}
  diverged more recently, around
  <strong>
    {printNodeAge(node.age)}.
  </strong>
{:else}diverged more recently.{/if}

{#if !isEmpty(additionalNodes)}
  Both belong to
  {#each additionalNodes as additionalNode, i}
    <InlineExternalLink
      href={`http://www.onezoom.org/life/@=${additionalNode.ott}`}
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
