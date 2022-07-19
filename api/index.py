import os
from backend import create_app
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN_BACKEND"),
    integrations=[FlaskIntegration()],
    traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", 1.0)),
)

app = create_app()
