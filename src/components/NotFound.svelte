<script>
  import { link } from 'svelte-routing'
</script>

<div class="center">
  <h1>How'd you get here?</h1>
  <a href="/" use:link>Go home</a>
</div>

<style lange="scss">
  .center {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
  }

  h1 {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }
</style>
