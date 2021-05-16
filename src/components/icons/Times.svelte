<script>
  export let size = undefined
</script>

<svg
  aria-hidden
  fill="none"
  height={size}
  width={size}
  viewBox="0 0 24 24"
  {...$$restProps}
>
  <path
    stroke-linecap="round"
    stroke-linejoin="round"
    d="M6 18L18 6M6 6l12 12"
  />
</svg>

<style type="text/scss">
  @import 'src/css/variables';

  svg {
    stroke: currentColor;
    stroke-width: 1.5;
  }
</style>
