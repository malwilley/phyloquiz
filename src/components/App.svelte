<script>
  import { Router, Route } from 'svelte-routing'
  import Home from '../modules/home/Home.svelte'
  import Play from '../modules/play/Play.svelte'
  import GenerateQuiz from '../modules/play/GenerateQuiz.svelte'
  import NotFound from './NotFound.svelte'
  import GlobalStyles from './GlobalStyles.svelte'
  import BackgroundImageBlurSvg from './BackgroundImageBlurSvg.svelte'
  import Notifications from '../modules/notification/Notifications.svelte'
</script>

<GlobalStyles />
<Router>
  <Route path="/"><Home /></Route>
  <Route path="/generate/:ott" let:params
    ><GenerateQuiz ott={params.ott} /></Route
  >
  <Route path="/quiz/:uuid" let:params><Play uuid={params.uuid} /></Route>
  <Route path="*"><NotFound /></Route>
</Router>

<Notifications />
<BackgroundImageBlurSvg />
