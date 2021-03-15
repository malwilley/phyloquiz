<script>
  import { slide, fly, fade } from 'svelte/transition'
  import { flip } from 'svelte/animate'
  import Notification from './Notification.svelte'
  import { notifications } from './store'
</script>

<div class="notifications">
  {#each $notifications as notification (notification.id)}
    <div
      class="notification-container"
      in:fly={{ y: 50, duration: 200 }}
      animate:flip={{ duration: 200 }}
    >
      <Notification {notification} />
    </div>
  {/each}
</div>

<style lang="scss">
  @import 'src/css/variables';

  .notifications {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding-bottom: 8rem;
    pointer-events: none;
    z-index: $z-index-notifications;
  }

  .notification-container {
    margin: 0 auto;
    max-width: 20rem;

    &:not(:last-child) {
      margin-bottom: 1rem;
    }
  }
</style>
