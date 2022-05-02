<template lang="pug">
v-container.d-flex.flex-column.align-center
  v-card.pa-6.d-flex.flex-column.small-container(flat outlined style='gap: 2rem')
    v-fade-transition
      v-overlay(absolute v-if='loadingConfigf')
        v-progress-circular(indeterminate)

    .d-flex
      v-btn.mr-2(icon @click='$router.back()')
        v-icon mdi-arrow-left
      h1.text-h6.font-weight-bold(style='margin-top: 2px')
        | {{ name && name.length ? name : (lamp ? lamp.name : 'Lamp') }} settings
      v-spacer
      transition(name='bounce')
        .d-flex.mt-2(v-hide='!saving')
          span.mr-2 Saving
          v-progress-circular.mt-1.ml-1(indeterminate size='20')

    //- Lamp name
    v-text-field(
      v-model='name'
      label='Lamp name'
      outlined
      dense 
      placeholder='My lamp'
      hide-details
    )

    //- Brightness level
    div
      h6.text-body-1 LED brightness level
      v-slider(
        v-model='config.brightness'
        discrete
        min='.25'
        max='1'
        step='.01'
        :label='Math.floor(config.brightness * 100) + "%"'
        hide-details
        @change='updateBrightness'
      )

    //- Reading light color temp
    div
      h6.text-body-1 Reading light color temperature
      .d-flex
        div(:style='`width: 12px; height: 12px; background: ${colorTempRGB}; border-radius: 50%; margin: 10px 8px 0 0`')
        v-slider(
          v-model='config.readingLightColorTemperature'
          label='Reading light color temperature'
          min='2100'
          max='10000'
          unit='K'
          :color='colorTempRGB'
          :label='`${config.readingLightColorTemperature} K`'
          @change='updateReadingLightColorTemperature'
          hide-details
        )

    //- Night mode
    div
      v-checkbox(
        v-model='config.nightMode'
        label='Night mode'
        color='primary'
        dense
        hide-details
        @change='updateNightMode'
      )
      p.text-caption.mt-2.mb-0 When enabled, the lamp will turn off when the room is dark.

      v-slide-y-transition
        div.mt-4(v-show='config.nightMode')
          h6.text-body-1 Minimum ambient light level (night mode)
          v-slider(
            v-model='config.minimumLightLevel'
            :disabled='!config.nightMode'
            discrete
            min='0'
            max='1'
            step='.1'
            :tick-labels="['Pitch black', '', '', '', '', 'Dark', '', '', '', '', 'Dim']"
            :label='config.minimumLightLevel * 100 + "%"'
            @change='updateMinimumLightLevel'
          )

    //- Motion detection
    div
      v-checkbox(
        v-model='config.motionDetection'
        label='Motion detection'
        color='primary'
        dense
        hide-details
        @change='updateMotionDetection'
      )
      p.text-caption.mt-2 When enabled, the lamp will only activate when motion is detected.

    
    v-sheet.d-flex.flex-column(style='background-color: rgba(255,0,0,.1)' rounded outlined)
      v-subheader.white--text
        span(style='margin: 0 8px 3px 0') ⚠️
        | Danger zone!
      v-divider(label='asdf')


      //- Delete lamp
      v-dialog(v-model='deleteLampDialog' max-width='500')
        template(v-slot:activator='{ on, attrs }')
          div
            v-btn.ma-4(color='error' @click='deleteLampDialog = true')
              v-icon(left) mdi-delete
              | Delete lamp
              
        v-card
          v-card-title.text-h5 Delete {{ name }}?
          v-card-text
            | Are you sure you want to delete this lamp?
          v-card-actions
            v-spacer
            v-btn(text @click='deleteLampDialog = false') Cancel
            v-btn(text color='error' @click='deleteLamp' :loading='deleting')
              v-icon(left) mdi-delete
              | Delete

</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator'
import { deleteLamp, getLamp, renameLamp, getLampConfig, updateLampConfig, LampConfig } from '@/services/lamp'
import { kelvinToRGB } from '@/util'

@Component
export default class LampSettings extends Vue {

  loadingConfig = false
  saving = false
  deleting = false
  deleteLampDialog = false

  name = ''
  config: any = {}
  
  async mounted() {
    const lamp = await getLamp(this.$route.params.id)
    this.name = lamp.name
    
    this.loadingConfig = true
    try {
      const config = await getLampConfig(lamp.deviceData.deviceId)
      if (config) {
        this.config = {
          ...this.config,
          ...config,
        }
      }
    }
    finally {
      this.loadingConfig = false
    }
  }

  get lamp() {
    return this.$store.getters.lamp(this.$route.params.id)
  }

  get colorTempRGB() {
    return kelvinToRGB(this.config.readingLightColorTemperature)
  }

  // Auto save name with debounce
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

  async updateBrightness(brightness: number) {
    this.updateConfig({ brightness })
  }

  async updateNightMode(nightMode: boolean) {
    this.updateConfig({ nightMode })
  }

  async updateMotionDetection(motionDetection: boolean) {
    this.updateConfig({ motionDetection })
  }

  async updateMinimumLightLevel(minimumLightLevel: number) {
    this.updateConfig({ minimumLightLevel })
  }

  async updateReadingLightColorTemperature(readingLightColorTemperature: number) {
    this.updateConfig({ readingLightColorTemperature })
  }

  async updateConfig(newVals: LampConfig) {
    this.saving = true
    try {
      await updateLampConfig(this.lamp.deviceData.deviceId, newVals)
    }
    finally {
      this.saving = false
    }
  }

  async deleteLamp() {
    this.deleting = true
    await deleteLamp(this.$route.params.id)
    this.deleting = false
    this.$router.push('/lamps')
  }
}
</script>

<style lang="scss">
.bounce-enter-active {
  animation: bounce-in 1s;
}
.bounce-leave-active {
  animation: bounce-in 1s reverse;
}
@keyframes bounce-in {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>