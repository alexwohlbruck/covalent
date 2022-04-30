<template lang="pug">
v-container
  v-card.pa-6.d-flex.flex-column(flat outlined style='gap: 2rem')
    .d-flex
      v-btn.mr-2(icon @click='$router.back()')
        v-icon mdi-arrow-left
      h1.text-h6.font-weight-bold(style='margin-top: 2px')
        | {{ name && name.length ? name : (lamp ? lamp.name : 'Lamp') }} settings
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

    //- Brightness level
    div
      h6.text-body-1 LED brightness level
      v-slider(
        v-model='settings.bightnessLevel'
        discrete
        min='.25'
        max='1'
        step='.01'
        :label='Math.floor(settings.bightnessLevel * 100) + "%"'
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
          h6.text-body-1 Minimum ambient light level (night mode)
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

    //- Reading light color temp
    div
      h6.text-body-1 Reading light color temperature
      v-slider(
        v-model='settings.readingLightColorTemperature'
        label='Reading light color temperature'
        min='2000'
        max='10000'
        unit='K'
        :color='colorTempRGB'
        :label='`${settings.readingLightColorTemperature} K`'
      )

    //- Delete lamp
    v-dialog(v-model='deleteLampDialog' max-width='500')
      template(v-slot:activator='{ on, attrs }')
        div
          v-btn(color='error' @click='deleteLampDialog = true')
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
import { deleteLamp, getLamp, renameLamp } from '@/services/lamp'
import { kelvinToRGB } from '@/util'

@Component
export default class LampSettings extends Vue {

  saving = false
  deleting = false
  deleteLampDialog = false

  name = ''
  settings = {
    nightMode: true,
    nightModeSensitivity: .5,
    bightnessLevel: 1,
    readingLightColorTemperature: 6000,
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
    return kelvinToRGB(this.settings.readingLightColorTemperature)
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


  async deleteLamp() {
    this.deleting = true
    await deleteLamp(this.$route.params.id)
    this.deleting = false
    this.$router.push('/lamps')
  }
}
</script>