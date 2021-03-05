<script>
  import ExternalLink from './icons/ExternalLink.svelte'

  export let href
</script>

<a {href} target="_blank" rel="noreferrer noopener"
  ><slot /><ExternalLink size={14} /></a
>

<style lang="scss">
  a {
    font-weight: bold;
    cursor: pointer;

    :global(svg) {
      margin-left: 0.1em;
    }
  }
</style>
