<script>
  import { isNil } from 'ramda'

  import EchoPillarbox from '../../../components/EchoPillarbox.svelte'
  import getVernacularOrName from '../../../utils/getVernacularOrName'

  export let leaf
  export let correct = null
  export let selected = false

  const getIucnDescriptionText = () => {
    switch (leaf.iucn) {
      case 'LC':
        return 'Least concern'
      case 'NT':
        return 'Near threatened'
      case 'VU':
        return 'Vulnerable'
      case 'EN':
        return 'Endangered'
      case 'CR':
        return 'Critically endangered'
      case 'EW':
        return 'Extinct in the wild'
      case 'EX':
        return 'Extinct'
      default:
        return ''
    }
  }
</script>

<div
  class="card main"
  class:correct={correct === true}
  class:incorrect={correct === false}
>
  <div class="image-container">
    <EchoPillarbox alt={`Image of ${leaf.name}`} src={leaf.thumbnail} />
    {#if selected}
      <div class="selected-badge">You selected</div>
    {/if}
  </div>
  <div class="text-container">
    {#if leaf.iucn}
      <div
        class="iucn-container iucn-badge iucn-badge-{leaf.iucn.toLowerCase()}"
        title={getIucnDescriptionText()}
      >
        {leaf.iucn}
      </div>
    {/if}
    <div class="links">
      {#if leaf.eol}
        <div class="link">
          <a
            class:disabled={isNil(leaf.eol)}
            href="https://eol.org/pages/{leaf.eol}"
            target="_blank"
            rel="noreferrer noopener">EOL</a
          >
        </div>
      {/if}
      <!-- {#if leaf.wikidata}
        <div class="link">
          <a
            class:disabled={isNil(leaf.wikidata)}
            href={`http://www.onezoom.org/life/@=${leaf.ott}`}
            target="_blank"
            rel="noreferrer noopener">Wikipedia</a
          >
        </div>
      {/if} -->
      {#if leaf.ott}
        <div class="link">
          <a
            class:disabled={isNil(leaf.ott)}
            href="http://www.onezoom.org/life/@={leaf.ott}"
            target="_blank"
            rel="noreferrer noopener">OneZoom</a
          >
        </div>
      {/if}
    </div>
    <div class="vernacular" class:scientific={isNil(leaf.vernacular)}>
      {getVernacularOrName(leaf)}{#if leaf.vernacular}{' '}<span class="name"
          >({leaf.name})</span
        >{/if}
    </div>
  </div>
</div>

<style type="text/scss">
  @import 'src/css/variables';
  @import 'src/css/media';

  .main {
    &.correct {
      box-shadow: 0 0 0 12px $primary-30;
    }

    &.incorrect {
      box-shadow: 0 0 0 12px $error-30;
    }

    @include for-phone-only {
      box-shadow: inset 0 0 0 1px $dark-20;
    }
  }

  .text-container {
    position: relative;
    padding: 0.5rem 1rem 1rem 1rem;
  }

  .vernacular {
    font-size: 1rem;
    font-weight: bold;
    text-transform: capitalize;
    white-space: pre-wrap;
    margin-top: 0.1rem;

    &.scientific {
      font-style: italic;
    }
  }

  .name {
    color: $text-color-light;
    font-weight: normal;
    font-style: italic;
  }

  .image-container {
    position: relative;
    height: 150px;
  }

  .selected-badge {
    position: absolute;
    top: 0.75rem;
    right: 0.75rem;

    display: inline-block;
    padding: 0.2rem 0.3rem;
    border-radius: 0.25rem;
    background: white;

    @include text-style-caps;
    letter-spacing: 0.3px;
    color: $text-color-dark;
    box-shadow: $box-shadow-small;
  }

  .iucn-container {
    position: absolute;
    right: 1rem;
    top: -1.5rem;
  }

  .iucn-badge {
    height: 2rem;
    width: 2rem;
    border-radius: 50%;
    background-color: $dark-600;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1px;
    font-family: $sans-serif-font;
    box-shadow: $box-shadow-small;
    border: 2px solid white;
    cursor: help;
  }

  .iucn-badge-lc {
    background-color: #007060;
  }

  .iucn-badge-nt {
    background-color: #007060;
  }

  .iucn-badge-vu {
    background-color: #e29b00;
  }

  .iucn-badge-en {
    background-color: #eb6209;
  }

  .iucn-badge-cr {
    background-color: #e40521;
  }

  .iucn-badge-ew,
  .iucn-badge-ex {
    background-color: #000101;
  }

  .links {
    display: flex;
    align-items: center;
    font-family: $sans-serif-font;

    .link {
      display: flex;
      align-items: center;

      a {
        display: flex;
        align-items: center;
        font-size: 0.75rem;
      }

      &:not(:last-child) {
        &::after {
          content: '⸱';
          color: $text-color-light;
          margin: 0 0.25rem;
        }
      }
    }
  }
</style>
