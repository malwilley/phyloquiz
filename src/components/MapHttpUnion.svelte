<script>
  export let value
</script>

{#if value?.type === 'notAsked' && $$slots.notAsked}
  <slot name="notAsked" />
{/if}
{#if value?.type === 'fetching' && $$slots.fetching}
  <slot name="fetching" />
{/if}
{#if value?.type === 'success' && $$slots.success}
  <slot name="success" />
{/if}
{#if value?.type === 'error' && $$slots.error}
  <slot name="error" />
{/if}

<slot />
