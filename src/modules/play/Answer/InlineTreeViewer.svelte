<script>
  import getVernacularOrName from '../../../utils/getVernacularOrName'
  import isPhoneViewport from '../../../utils/isPhoneViewport'

  export let node = null

  let show = !isPhoneViewport()

  $: url = `https://onezoom.org/life/@=${node?.ott}`
  $: name = getVernacularOrName(node)

  const handleLoadClick = () => {
    show = true
  }
</script>

{#if node}
  <div class="iframe-container">
    {#if show}
      <iframe
        src={url}
        sandbox="allow-scripts allow-same-origin"
        title="Inline tree viewer"
      />
    {:else}
      <div class="unloaded-content">
        <div class="unloaded-heading">Inline Tree Viewer</div>
        <div class="unloaded-description">
          Delve into <strong>{name}</strong> in the OneZoom tree of life
          explorer.<br /><a href={url} target="_blank" rel="noopener noreferrer"
            >Or open in a new tab.</a
          >
        </div>
        <button class="button" on:click={handleLoadClick}>Tap to load</button>
      </div>
    {/if}
  </div>
{/if}

<style lang="scss">
  @import 'src/css/variables';
  @import 'src/css/media';

  .iframe-container {
    height: 30rem;
    margin-top: 5rem;
    background: white;
    box-shadow: $box-shadow-card;

    position: relative;
  }

  .unloaded-content {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 100%;
    max-width: 16rem;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;

    font-family: $sans-serif-font;
    font-size: 0.9rem;
    line-height: 1.5;
    text-align: center;
  }

  .unloaded-heading {
    font-weight: bold;
    font-size: 1.25rem;
  }

  .unloaded-description {
    color: $text-color-light;
    margin: 1rem 0;
  }

  .button {
    margin-top: 3rem;
  }

  iframe {
    width: 100%;
    height: 100%;
  }
</style>
