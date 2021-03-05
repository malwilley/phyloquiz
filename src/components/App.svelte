<script>
  import { Router, Route } from 'svelte-routing'
  import Home from '../modules/home/Home.svelte'
  import Play from '../modules/play/Play.svelte'
  import NotFound from './NotFound.svelte'
  import GlobalStyles from './GlobalStyles.svelte'
  import BackgroundImageBlurSvg from './BackgroundImageBlurSvg.svelte'
</script>

<GlobalStyles />
<Router>
  <Route path="/play/:ott" let:params><Play ott={params.ott} /></Route>
  <Route path="/"><Home /></Route>
  <Route path="*"><NotFound /></Route>
</Router>

<BackgroundImageBlurSvg />
