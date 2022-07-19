#!/bin/sh

# CI build script
# Releases a Sentry version on prod build

SENTRY_CLI=./node_modules/@sentry/cli/bin/sentry-cli

if [ "$VERCEL_ENV" = "production" ]
then
  echo "Creating Sentry release..."

  # Get a version string
  VERSION=`$SENTRY_CLI releases propose-version`

  # Start release
  $SENTRY_CLI releases new "$VERSION" -p phyloquiz-client
  $SENTRY_CLI releases new "$VERSION" -p phyloquiz-backend

  # Upload source maps
  $SENTRY_CLI releases files "$VERSION" upload-sourcemaps dist -p phyloquiz-client
else
  echo "Skipping Sentry release..."
fi

# Do the build
yarn build

if [ "$VERCEL_ENV" = "production" ]
then
  # Finalize version
  $SENTRY_CLI releases finalize "$VERSION" -p phyloquiz-client
  $SENTRY_CLI releases finalize "$VERSION" -p phyloquiz-backend
fi
