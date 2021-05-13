<script>
  import MapHttpUnion from '../../components/MapHttpUnion.svelte'
  import CenterContent from '../../components/CenterContent.svelte'
  import { actions, featuredNodes } from './store'
  import { link } from 'svelte-routing'
  import { fade } from 'svelte/transition'
  import { onMount } from 'svelte'
  import QuizSearch from './QuizSearch.svelte'
  import Footer from './Footer.svelte'

  onMount(() => {
    window.scrollTo(0, 0)
    actions.fetchFeatured()
  })
</script>

<div class="main" in:fade>
  <section class="search-hero">
    <h1 class="large-text">Generate a quiz from any category of life.</h1>
    <QuizSearch />
  </section>

  <div class="body">
    <CenterContent>
      <section>
        <MapHttpUnion value={$featuredNodes}>
          <div slot="success">
            <div class="quiz-cards-container">
              {#each $featuredNodes.data as node, i}
                <div
                  class="card quiz-card"
                  in:fade={{ delay: i * 150, duration: 600 }}
                >
                  <div class="quiz-card-images">
                    {#each node.images as imageUrl, i}
                      <img
                        class="quiz-card-image"
                        alt="Representative species {i + 1}"
                        src={imageUrl}
                      />
                    {/each}
                  </div>
                  <div class="quiz-card-text">
                    <div class="quiz-card-vernacular">
                      {node.vernacular}
                    </div>
                  </div>
                  <div class="quiz-card-footer">
                    <div class="num-species">
                      {node.numSpecies.toLocaleString()}
                      playable species
                    </div>
                    <a
                      class="quiz-card-play"
                      href="/generate/{node.ott}"
                      use:link
                    >
                      Play
                    </a>
                  </div>
                </div>
              {/each}
            </div>
          </div>
          <div slot="error">
            <div>Error! {$featuredNodes?.message}</div>
          </div>
        </MapHttpUnion>
      </section>
    </CenterContent>
  </div>
</div>

<Footer />

<style type="text/scss">
  @import 'src/css/variables';
  @import 'src/css/media';

  .main {
    min-height: 100vh;
  }

  .search-hero {
    display: grid;
    grid-template-areas:
      'search'
      'text';
    gap: 3rem;
    position: relative;
    padding: 2rem 1rem 0 1rem;
    align-items: center;
    justify-items: center;

    @include for-tablet-portrait-up {
      padding: 6rem 1rem 0 1rem;
      grid-template-areas:
        'text'
        'search';
    }

    @include for-tablet-landscape-up {
      padding: 10rem 1rem 0 1rem;
    }

    @include for-desktop-up {
      padding: 20vh 1rem 0 1rem;
    }
  }

  .large-text {
    grid-area: text;
    font-size: 2.25rem;
    font-weight: bold;
    display: block;
    line-height: 1.25;
    text-align: center;

    // To blur out background
    background-color: rgba($primary-10, 0.5);
    border-radius: 1rem;
    box-shadow: 0 0 1rem $primary-10;

    @include for-tablet-portrait-up {
      font-size: 2.5rem;
    }
  }

  .body {
    position: relative;
    z-index: 2;
    padding: 4rem 0;
  }

  .quiz-cards-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1rem;

    @include for-tablet-landscape-up {
      margin-top: 2rem;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-wrap: wrap;

      gap: 0;

      .quiz-card {
        margin: 0 1.25rem 1.25rem 0;
        width: 20rem;
      }
    }
  }

  .quiz-card {
    position: relative;
    height: auto;
    transition: 200ms box-shadow ease-out;

    &:hover {
      box-shadow: inset 0 0 0 1px $primary-30, $box-shadow-card-no-outline;
    }
  }

  .quiz-card-text {
    padding: 0 1.25rem;
  }

  .quiz-card-vernacular {
    text-transform: capitalize;
    font-weight: bold;
    font-size: 1.25rem;
    color: $text-color-dark;

    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }

  .quiz-card-play {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    letter-spacing: 0.3px;
    color: $dark-600;
    height: 1.6rem;
    border-radius: 0.8rem;
    border: 1px solid $dark-20;
    padding: 0 1rem;
    font-weight: bold;
    font-family: $sans-serif-font;

    background-color: white;
    transition: all 200ms ease-out;

    &:hover,
    &:focus {
      text-decoration: none;
      background-color: $primary-60;
      color: white;
      border: 1px solid $primary-60;
    }

    &:active {
      box-shadow: 0 0 0 0.25rem rgba($primary-60, 0.3);
    }

    &::after {
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
    }
  }

  .quiz-card-images {
    display: flex;
    overflow: hidden;
    padding: 0 1rem;
    margin: 1rem 0 0 0;
    height: 3rem;
    flex-wrap: wrap;
  }

  .quiz-card-image {
    height: 2.6rem;
    width: 2.6rem;
    border-radius: 1.3rem;
    border: 3px solid white;
    display: block;
    background-color: $dark-20;
    color: transparent;
    box-sizing: border-box;

    &:not(:first-child) {
      margin-left: -1rem;
    }
  }

  .quiz-card-footer {
    padding: 0 1.25rem 1rem 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .num-species {
    font-family: $sans-serif-font;
    font-size: 0.7rem;
    color: $text-color-light;
  }

  @media (max-width: 24rem) {
    .quiz-cards-container {
      grid-template-columns: 1fr;
    }
  }
</style>
