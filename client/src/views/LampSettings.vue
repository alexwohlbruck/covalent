<template lang="pug">
v-container.d-flex.flex-column(style='gap: 2rem')
  .d-flex
    h1.text-h4.font-weight-bold {{ name && name.length ? name : (lamp ? lamp.name : 'Lamp') }} settings
    v-spacer
    .d-flex(v-if='saving')
      span.mr-2 Saving
      v-progress-circular(indeterminate size='20')
    

  //- Lamp name
  v-text-field(
    v-model='name'
    label='Lamp name'
    outlined
    dense 
    placeholder='My lamp'
    hide-details
  )

  //- Night mode
  div
    v-checkbox(
      v-model='settings.nightMode'
      label='Night mode'
      color='primary'
      dense
      hide-details
    )
    p.text-caption.mt-2 When enabled, the lamp will turn off when the room is dark.

    v-slide-y-transition
      div(v-show='settings.nightMode')
        h6.text-body-1 Minimum light level
        v-slider(
          v-model='settings.nightModeSensitivity'
          :disabled='!settings.nightMode'
          discrete
          min='0'
          max='1'
          step='.1'
          :tick-labels="['Pitch black', '', '', '', '', 'Dark', '', '', '', '', 'Dim']"
          :label='settings.nightModeSensitivity * 100 + "%"'
        )

  //- Touch panel sensitivity
  div
    h6.text-body-1 Touch panel sensitivity
    v-slider(
      v-model='settings.touchPanelSensitivity'
      discrete
      min='0'
      max='1'
      step='.1'
      :tick-labels="['Light touch', '', '', '', '', 'Normal touch', '', '', '', '', 'Heavy press']"
      :label='settings.touchPanelSensitivity * 100 + "%"'
    )

  //- Reading light color temp
  div
    h6.text-body-1 Reading light color temperature
    v-slider(
      v-model='settings.readingLightColorTemp'
      label='Reading light color temperature'
      min='2000'
      max='10000'
      unit='K'
      :color='colorTempRGB'
      :label='`${settings.readingLightColorTemp} K`'
    )

  //- Delete lamp
  div
    v-btn(color='error')
      v-icon(left) mdi-delete
      | Delete lamp
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator'
import { getLamp, renameLamp } from '@/services/lamp'
import { kelvinToRGB } from '@/util'

@Component
export default class LampSettings extends Vue {

  saving = false

  name = ''
  settings = {
    nightMode: true,
    nightModeSensitivity: .5,
    touchPanelSensitivity: .5,
    readingLightColorTemp: 6000,
  }
  
  async mounted() {
    const lamp = await getLamp(this.$route.params.id)

    this.name = lamp.name
    // this.fields.settings = lamp.settings
  }

  get lamp() {
    return this.$store.getters.lamp(this.$route.params.id)
  }

  get colorTempRGB() {
    return kelvinToRGB(this.settings.readingLightColorTemp)
  }

  // Auto save with debounce
  nameTimeout: any = null
  @Watch('name')
  async onNameChange() {
    if (this.nameTimeout) {
      clearTimeout(this.nameTimeout)
    }
    this.nameTimeout = setTimeout(async () => {
      this.saving = true
      await renameLamp(this.$route.params.id, this.name)
      this.saving = false
    }, 500)
  }


}
</script>