<template lang="pug">
v-card.lamp-card(light)
  v-card-text.d-flex.flex-column.flex-row
    .d-flex
      div
        .text-h5.font-weight-bold(:style='`color: ${state.colors[0]}`')
          | {{ lamp.name }}
        .text-body-2.font-weight-bold {{ lamp.user.name }}

      v-spacer
      v-btn(
        v-if='isMyLamp'
        icon
        color='black'
        :to="{name: 'lamp-settings', params: {id: lamp._id}}"
      )
        v-icon mdi-cog

    .d-flex.align-sm-end.justify-space-between.flex-column.flex-sm-row
      v-spacer(v-if='!isMyLamp')

      lamp-visualizer.mb-4(
        :state='state'
        :lampId='lamp._id'
        :small='!isMyLamp'
      )
      v-btn.px-8.py-7(
        v-if='isMyLamp'
        @mousedown='activate'
        @touchstart='activate'
        @mouseup='deactivate'
        @mouseleave='deactivate'
        @touchend='deactivate'
        @touchcancel='deactivate'
        dark
        :style='`background: ${gradientFromHue(selectedColor.h)}; box-shadow: ${colorShadow(selectedColor.h)}; transition: none;`'
      )
        | Send pulse
  
  v-color-picker(
    v-if='isMyLamp'
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
import { gradientFromHue, hslToHexString, colorShadow } from '@/util'

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
  @Prop({ default: null }) state: any

  touching = false
  selectedColor: Hsl = {
    h: 0,
    s: 1,
    l: 0.5,
  }

  get isMyLamp() {
    return this.lamp?.user._id === this.$store.getters.me?._id
  }

  gradientFromHue(hue: number) {
    return gradientFromHue(hue, 'to right')
  }

  colorShadow(hue: number) {
    return colorShadow(hue)
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