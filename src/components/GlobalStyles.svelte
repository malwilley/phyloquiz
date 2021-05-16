<script></script>

<style global lang="scss">
  @import 'src/css/variables';
  @import 'src/css/reset';

  html {
    background-color: $dark-10;
    color: $text-color-dark;
    box-sizing: border-box;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
      Oxygen-Sans, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
    font-family: $serif-font;
    overflow-y: scroll;
  }

  body {
    min-height: 100vh;
    overflow: hidden;
  }

  a {
    color: $link-blue;
    text-decoration: none;
  }

  a:hover {
    text-decoration: underline;
  }

  a:visited {
    color: $link-blue;
  }

  label {
    display: block;
  }

  input,
  textarea {
    color: $text-color-dark;

    &::placeholder {
      color: $text-color-light;
      opacity: 1;
    }
  }

  input,
  button,
  select,
  textarea {
    font-family: inherit;
    font-size: inherit;
    -webkit-padding: 0;
    padding: 0;
    margin: 0;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 2px;
    outline: none;

    font-family: $sans-serif-font;

    -webkit-tap-highlight-color: transparent;

    &:focus {
      outline: none;
    }
  }

  button {
    cursor: pointer;
    background: transparent;
    border: none;

    &:focus {
      color: inherit;
    }
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    margin: 0;
  }

  hr {
    border: 0;
    height: 1px;
    background-color: $dark-20;
    margin: 1rem 0;
  }

  .visually-hidden {
    clip: rect(0 0 0 0);
    clip-path: inset(50%);
    height: 1px;
    overflow: hidden;
    position: absolute;
    white-space: nowrap;
    width: 1px;
  }

  .center-content {
    margin: 0 auto;
    max-width: 72rem;
    padding: 0 1rem;
  }

  .card {
    position: relative;
    box-shadow: $box-shadow-card;
    border-radius: 1rem;
    overflow: hidden;
    width: 100%;
    background-color: white;
  }

  .button {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: $primary-90;
    border-radius: 1.625rem;
    font-family: $sans-serif-font;
    color: white;
    padding: 0 2rem;
    height: 3.25rem;
    font-weight: bold;
    transition: box-shadow 200ms, background-color 200ms;

    &:disabled {
      background-color: $dark-50;
      box-shadow: none;
      color: $dark-10;
      cursor: disabled;
    }

    &:focus,
    &:active,
    &:hover,
    &:visited {
      color: white;
      text-decoration: none;
    }

    &:not(:disabled):hover {
      background-color: lighten($primary-90, 5%);
    }

    &:not(:disabled):active {
      background-color: darken($primary-90, 5%);
    }

    &:not(:disabled):focus {
      box-shadow: 0 0 0 6px $primary-30;
    }

    // Secondary styles
    &.secondary {
      background: none;
      color: $text-color-light;
      box-shadow: none;
      transition: box-shadow 200ms, background-color 200ms, color 200ms;

      &:not(:disabled):hover {
        background-color: transparent;
        color: $text-color-dark;
      }

      &:not(:disabled):active {
        background-color: $dark-10;
        color: $text-color-dark;
      }

      &:not(:disabled):focus {
        background-color: $dark-10;
      }
    }

    svg {
      width: 1.3em;
      height: 1.3em;

      &:first-child {
        margin-right: 0.5em;
        margin-left: -0.5em;
      }

      &:last-child {
        margin-left: 0.5em;
        margin-right: -0.5em;
      }
    }
  }

  .error-text {
    font-family: $sans-serif-font;
    color: $text-color-error;
  }

  @media (prefers-reduced-motion: reduce) {
    * {
      animation-delay: 0ms !important;
      animation-duration: 1ms !important;
    }
  }
</style>
