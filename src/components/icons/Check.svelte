<script>
  export let size = undefined
</script>

<svg
  fill="none"
  height={size}
  width={size}
  viewBox="0 0 24 24"
  stroke="currentColor"
  {...$$restProps}
>
  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
</svg>

<style type="text/scss">
  @import 'src/css/variables';

  svg {
    stroke: currentColor;
    stroke-width: 1.5;
  }
</style>
