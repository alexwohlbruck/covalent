<template lang="pug">
.lamp-visualizer
  //- div(:style='`width: 100px; height: 100px; background: ${state.colors[0]}`')

  .lamp
    .section.lid(style='z-index: 3;')
      .bottom
      .middle
      .top
      
    .section.light(style='z-index: 2;')
      .bottom(:style='`background: ${state.colors[0]}`')
      .middle(:style='`background: ${state.colors[0]}`')

    .section.base(style='z-index: 1;')
      .bottom
      .middle

</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import { GroupState } from '@/types/Group'


type State = GroupState

@Component
export default class LampVisualizer extends Vue {
  @Prop(Object) state!: State
}
</script>

<style lang="scss">

$lamp-width: 10em;
$lamp-height: 15em;
$perspective: 3em;

$lid-height: .04 * $lamp-height;
$light-height: .76 * $lamp-height;
$base-height: .2 * $lamp-height;

.lamp {
  position: relative;
  width: $lamp-width;
  height: $lamp-height;
  margin-bottom: $lamp-height * .23;
  
  .section {
    position: relative;
    width: $lamp-width;
    top: $lid-height;

    .top{
      position: absolute;
      width: $lamp-width;
      height: $perspective;
      border-radius: 50%;
      background-color: rgb(214, 214, 214);
    }

    .middle {
      position: absolute;
      top: $perspective / 2;
      width: $lamp-width;
      background-color: rgb(161, 161, 161);
    }
    .bottom {
      content: '';
      position: absolute;
      left: 0;
      width: $lamp-width;
      height: $perspective;
      border-radius: 50%;
      background-color: rgb(161, 161, 161);
    }
  }

  .lid {
    .top {
      top: 0;
    }
    .middle {
      top: $perspective / 2;
      height: $lid-height;
    }
    .bottom {
      top: $lid-height;
    }
  }

  .light {
    .middle {
      top: $perspective / 2 + $lid-height;
      height: $light-height;
    }
    .bottom {
      top: $lid-height + $light-height;
    }
    .middle, .bottom {
      background-color: red;
    }
  }

  .base {
    .middle {
      top: $perspective / 2 + $lid-height + $light-height;
      height: $base-height;
    }
    .bottom {
      top: $lid-height + $light-height + $base-height;
    }
    .middle, .bottom {
      background-color: rgb(207, 109, 43);
    }
  }

}
</style>
