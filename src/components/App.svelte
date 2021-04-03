<script>
  import { Router, Route } from 'svelte-routing'
  import Home from '../modules/home/Home.svelte'
  import Play from '../modules/play/Play.svelte'
  import GenerateQuiz from '../modules/play/GenerateQuiz.svelte'
  import NotFound from './NotFound.svelte'
  import GlobalStyles from './GlobalStyles.svelte'
  import BackgroundImageBlurSvg from './BackgroundImageBlurSvg.svelte'
  import Notifications from '../modules/notification/Notifications.svelte'
  import { fade } from 'svelte/transition'
</script>

<GlobalStyles />
<Router>
  <Route path="/"><Home /></Route>
  <Route path="/generate/:ott" let:params>
    <div out:fade>
      <GenerateQuiz ott={params.ott} />
    </div>
  </Route>
  <Route path="/quiz/:uuid" let:params><Play uuid={params.uuid} /></Route>
  <Route path="*"><NotFound /></Route>
</Router>

<Notifications />
<BackgroundImageBlurSvg />
