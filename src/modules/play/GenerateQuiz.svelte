<script>
  import { generateQuiz } from '../../api/generateQuiz'
  import CenterContent from '../../components/CenterContent.svelte'
  import PhyloLoader from '../../components/PhyloLoader.svelte'
  import { navigate } from 'svelte-routing'
  import { actions } from './store'
  import { fade } from 'svelte/transition'

  export let ott

  const tryGenerateQuiz = async () => {
    const uuid = await generateQuiz(ott)
    await actions.getQuiz(uuid)
    navigate(`/quiz/${uuid}`, { replace: true })
  }

  let generatePromise = tryGenerateQuiz()

  const retry = () => {
    generatePromise = tryGenerateQuiz()
  }
</script>

{#await generatePromise}
  <div class="loading" out:fade>
    <PhyloLoader>Generating quiz...</PhyloLoader>
  </div>
{:catch}
  <CenterContent>
    <div class="error-content">
      <p class="error">Something went during quiz generation.</p>
      <button class="button" on:click={retry}>Click to try again</button>
    </div>
  </CenterContent>
{/await}

<style lang="scss">
  @import 'src/css/variables';

  .loading {
    position: absolute;
    left: 0;
    top: 50%;
    width: 100%;
    transform: translateY(-50%);
  }

  .error-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-top: 8rem;
  }

  .error {
    font-weight: bold;
    font-family: $sans-serif-font;
    margin-bottom: 2rem;
    line-height: 2;
  }
</style>
