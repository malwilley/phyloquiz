<script>
  import Times from '../../components/icons/Times.svelte'
  import { actions } from './store'

  export let notification
</script>

<div class="notification" class:error={notification.type === 'error'}>
  <div class="message">
    {notification.message}
  </div>
  <button
    class="close-button"
    on:click={() => actions.popNotification(notification.id)}
  >
    <Times size={16} />
  </button>
</div>

<style lang="scss">
  @import 'src/css/variables';

  .notification {
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    background-color: $dark-600;
    color: white;
    display: flex;
    justify-content: space-between;
    pointer-events: all;

    box-shadow: $box-shadow-medium;

    &.error {
      background-color: $error-300;
    }
  }

  .message {
    min-width: 0;
    font-family: $sans-serif-font;
    font-size: $sans-serif-size-medium;
    line-height: 1.5;
    padding-right: 1rem;
  }

  .close-button {
    display: flex;
    align-items: center;
    justify-content: center;

    background-color: rgba(white, 0.2);
    height: 2rem;
    width: 2rem;
    border-radius: 0.25rem;
    flex-shrink: 0;
    color: white;

    &:hover {
      background-color: rgba(white, 0.3);
    }

    :global(svg) {
      stroke-width: 3;
    }
  }
</style>
