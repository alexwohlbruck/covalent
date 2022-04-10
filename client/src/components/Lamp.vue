<template lang="pug">
v-card(light)
  v-card-text.d-flex.flex-column
    .d-flex
      .text-h5.font-weight-bold(:style='`color: ${lamp.group.state.colors[0]}`')
        | {{ lamp.name }}

      v-spacer
      v-btn(icon color='black' :to="{name: 'lamp-settings', params: {id: lamp._id}}")
        v-icon mdi-cog

    .d-flex.align-sm-end.justify-space-between.flex-column.flex-sm-row
      lamp-visualizer.mb-4(
        :state='lamp.group.state'
        :lampId='lamp._id'
      )
      v-btn.px-8.py-7(
        @mousedown='activate'
        @touchstart='activate'
        @mouseup='deactivate'
        @mouseleave='deactivate'
        @touchend='deactivate'
        @touchcancel='deactivate'
        dark
        :style='`background: ${gradientFromHue(selectedColor.h)}`'
      )
        | Send pulse
  
  v-color-picker(
    v-model='selectedColor'
    hide-canvas
    hide-inputs
    swatches-max-height='200'
  )
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import LampVisualizer from '@/components/LampVisualizer.vue'
import { sendCommand } from '@/services/lamp'
import { gradientFromHue, hslToHexString } from '@/util'

type Hsl = {
  h: number
  s: number
  l: number
}

@Component({
  components: {
    LampVisualizer,
  },
})
export default class Lamp extends Vue {
  @Prop({ default: null }) lamp: any

  touching = false
  selectedColor: Hsl = {
    h: 0,
    s: 1,
    l: 0.5,
  }

  gradientFromHue(hue: number) {
    return gradientFromHue(hue, 'to right')
  }

  activate() {
    this.updateLamp(true)
  }

  deactivate() {
    this.updateLamp(false)
  }

  async updateLamp(touching: boolean) {
    this.touching = touching

    const { h, s, l } = this.selectedColor

    await sendCommand({
      lampId: this.lamp._id,
      touching,
      color: hslToHexString(h, s*100, l*100),
    })
  }
}
</script>

<style lang="scss">
$picker-height: 3rem;
$thumb-width: .4rem;

.v-color-picker {
  max-width: unset !important;
  border-top-right-radius: 0 !important;
  border-top-left-radius: 0 !important;

  .v-color-picker__controls {
    padding: 0 2rem;
    background: red;
  }

  .v-input__slider {
    border-radius: 0 !important;
  }

  .v-slider {
    padding: $picker-height / 2;
  }

  .v-color-picker__dot {
    display: none;
  }

  .v-slider__thumb {
    height: $picker-height * 1.2;
    width: $thumb-width;
    border-radius: $thumb-width;

    &::before {
      display: none;
    }
  }

  .v-slider__thumb-container--active {
    .v-slider__thumb {
      width: $thumb-width * 1.3;
    }
  }
}
</style>