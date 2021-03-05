<script>
  import { isNil } from 'ramda'

  import getVernacularOrName from '../../../utils/getVernacularOrName'

  export let leaf

  const name = getVernacularOrName(leaf)
</script>

<span class:scientific={isNil(leaf.vernacular)}>
  {name}
</span>

<style lang="scss">
  @import 'src/css/media';

  span {
    font-size: 0.9rem;

    @include for-tablet-portrait-up {
      font-size: 1.25rem;
    }

    &.scientific {
      font-style: italic;
    }
  }
</style>
