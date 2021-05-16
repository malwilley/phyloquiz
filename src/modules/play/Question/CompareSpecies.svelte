<script>
  import EchoPillarbox from '../../../components/EchoPillarbox.svelte'
  import QuestionSpeciesLabel from './QuestionSpeciesLabel.svelte'

  export let species

  const name = species?.vernacular ?? species?.name ?? 'Unknown'
</script>

<div class="main">
  <div class="image-card card">
    <img alt={`Image of ${name}`} class="image" src={species.thumbnail} />
  </div>

  <div class="card name">
    <QuestionSpeciesLabel leaf={species} />
  </div>
</div>

<style type="text/scss">
  @import 'src/css/variables';
  @import 'src/css/media';

  .main {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin-bottom: 1rem;

    @include for-tablet-portrait-up {
      margin-bottom: 2rem;
    }
  }

  .name {
    display: flex;
    justify-content: center;
    align-items: center;

    margin-top: 1em;
    font-size: 1rem;
    font-weight: bold;
    text-align: center;
    text-transform: capitalize;
    min-height: 3rem;
    border-radius: 0.5rem;
    padding: 0 2rem;
    width: auto;

    font-size: 0.9rem;

    @include for-tablet-portrait-up {
      font-size: 1.25rem;
    }
  }

  .image-card {
    height: 150px;
    width: 150px;
  }

  .image {
    height: 100%;
    width: 100%;
  }
</style>
