<template lang="pug">
div
  span.flex-shrink-1.lamp(
    :style='visualizerStyle'
    :class='{pulse: incomingMessage, active: state.active}'
    @mousedown='updateLamp(true)'
    @touchstart='updateLamp(true)'
    @mouseup='updateLamp(false)'
    @touchend='updateLamp(false)'
  )
  pre {{ state }}
  
  //- Color picker
  //- .d-flex.flex-column.align-center
  //-   .d-flex
  v-slider(
    style='width: 150px'
    v-model='hue'
    min='0'
    max='360'
    :color='selectedColor'
    :track-color='shiftedColor'
  )
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'vue-property-decorator'
import { hslToHexString, hexStringToHsl } from '@/util'
import { LampState } from '@/types/Lamp'
import { GroupState } from '@/types/Group'
import { sendCommand } from '@/services/lamp'

let timeout: any

type State = GroupState

@Component
export default class LampVisualizer extends Vue {

  @Prop(Object) state!: State
  @Prop(String) lampId!: string
  @Prop(Boolean) active!: boolean

  hue = 0
  cooldown = false
  touching = false

  get incomingMessage() {
    return this.state.active && !this.touching
  }

  @Watch('state')
  onStateChanged() {
    this.cooldown = (this.state as any).active
    // this.cooldown = true
    // clearTimeout(timeout)
    // timeout = setTimeout(() => {
    //   this.cooldown = false
    // }, 10000)
  }

  get visualizerStyle() {

    if (!this.state) {
      return {}
    }

    let colors = this.state.colors

    colors = [...colors]

    const firstColor = colors[0]

    if (colors.length == 1) {
      // Add a second color that is slightly shifted
      const hsl = hexStringToHsl(firstColor)
      hsl[0] = hsl[0] + 40
      const shiftedColor = hslToHexString(...hsl)
      colors.push(shiftedColor)
    }

    return {
      'box-shadow': `0px 0px 50px 30px ${firstColor}`,
      background: `black linear-gradient(135deg, ${colors.join(',')})`,
    }
  }
  
  get selectedColor(): string {
    return hslToHexString(this.hue, 100, 50)
  }

  get shiftedColor(): string {
    const hsl = hexStringToHsl(this.selectedColor)
    hsl[0] = hsl[0] + 40
    return hslToHexString(...hsl)
  }

  async updateLamp(touching: boolean) {
    this.touching = touching

    await sendCommand({
      lampId: this.lampId,
      touching,
      color: this.selectedColor,
    })
  }
}
</script>

<style lang="scss">
@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.7;
  }
  20% {
    transform: scale(1.1);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 0.7;
  }
}

$size: 200px;

.lamp {
  display: block;
  margin: 50px 0;
  width: $size;
  height: $size;
  border-radius: 50%;
  transition: all 1s ease;
  opacity: 0.2;

  &.active {
    opacity: 1;
  }

  &.pulse {
    animation: pulse 1s ease-in-out infinite;
  }
}
</style>
