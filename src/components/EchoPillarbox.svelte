<script>
  export let src
  export let alt
</script>

<div class="echo-pillarbox" {...$$restProps}>
  <img class="background-image" {alt} {src} />
  <img class="foreground-image" aria-hidden alt="" {src} />
  <slot />
</div>

<style type="text/scss">
  @import 'src/css/variables';
  @import 'src/css/media';

  .echo-pillarbox {
    position: relative;
    overflow: hidden;
    height: 100%;
  }

  .background-image {
    position: absolute;
    left: 0;
    top: 50%;
    filter: $bg-image-filter;
    width: 100%;
    transform: translateY(-50%);
    pointer-events: none;

    @include for-phone-only {
      filter: brightness(50%) saturate(30%);
    }
  }

  .foreground-image {
    height: 100%;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    top: 0;
  }
</style>
