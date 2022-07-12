import App from './components/App.svelte'

import * as Sentry from '@sentry/browser'
import { BrowserTracing } from '@sentry/tracing'

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  integrations: [new BrowserTracing()],
  tracesSampleRate: Number(process.env.SENTRY_TRACES_SAMPLE_RATE),
})

const app = new App({
  target: document.body,
})

export default app
