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
    transition: box-shadow 200ms ease-out, background-color 200ms ease-out;

    box-shadow: 0 0.25rem 0.25rem 0 rgba($dark-600, 0.1),
      0 0.5rem 0.5rem 0 rgba($dark-600, 0.05);

    &:disabled {
      background-color: $dark-50;
      box-shadow: none;
      color: $dark-10;
      cursor: disabled;
    }

    &:focus,
    &:active,
    &:hover {
      color: white;
      text-decoration: none;
    }

    &:enabled:hover {
      background-color: lighten($primary-90, 5%);
    }

    &:enabled:active {
      background-color: darken($primary-90, 5%);
    }

    &:enabled:focus {
      box-shadow: 0 0 0 6px $primary-30,
        0 0.25rem 0.25rem 0 rgba($dark-600, 0.1),
        0 0.5rem 0.5rem 0 rgba($dark-600, 0.05);
    }

    // Secondary styles
    &.secondary {
      background: none;
      color: $text-color-light;
      box-shadow: none;
      transition: color 200ms ease-out;

      &:hover {
        color: $text-color-dark;
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
</style>
