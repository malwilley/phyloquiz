<script>
  export let size = undefined
  export let direction

  const calculateRotation = (direction) => {
    switch (direction) {
      case 'up':
        return 270
      case 'right':
        return 0
      case 'down':
        return 90
      case 'left':
        return 180
      default:
        return 0
    }
  }

  $: rotation = calculateRotation(direction)
</script>

<svg
  viewBox="0 0 24 24"
  height={size}
  width={size}
  transform={`rotate(${rotation})`}
  fill="none"
  {...$$restProps}
>
  <path
    stroke-linecap="round"
    stroke-linejoin="round"
    d="M14 5l7 7m0 0l-7 7m7-7H3"
  />
</svg>

<style type="text/scss">
  @import 'src/css/variables';

  svg {
    stroke: currentColor;
    stroke-width: 2.5;
  }
</style>
