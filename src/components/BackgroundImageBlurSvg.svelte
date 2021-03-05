<script>
  /**
   * Reference this when blurring images in CSS with `filter: url(#bg-image-blur)`
   * This results in a blurred image with a sharp outline which is not the case with simple CSS blurring.
   * https://codepen.io/johndjameson/pen/xVjgPy
   */
</script>

<svg class="visually-hidden">
  <filter id="bg-image-blur">
    <feGaussianBlur stdDeviation="32" />
    <feColorMatrix
      type="matrix"
      values="1 0 0 0 0, 0 1 0 0 0, 0 0 1 0 0, 0 0 0 9 0"
    />
    <feComposite in2="SourceGraphic" operator="in" />
  </filter>
</svg>
