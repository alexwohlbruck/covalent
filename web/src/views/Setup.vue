<template lang="pug">

v-container
  v-stepper(v-model='step' vertical)

    //- Bluetooth pairing
    v-stepper-step(:complete='step > 1' step='1') Connect to your lamp

    v-stepper-content(step='1')
      v-sheet(color='transparent')
        v-card-text Allow Bluetooth access and then connect to your lamp in the devices list.
        v-card-text
          v-btn(@click='pairBluetooth' color='blue darken-1') Pair with bluetooth

    //- Wifi config
    v-stepper-step(:complete='step > 2' step='2') Configure analytics for this app

    v-stepper-content(step='2')
      v-card.mb-12(color='grey lighten-1' height='200px')
      v-btn(color='primary' @click='step = 3') Continue
      v-btn(text='') Cancel

    //- Group config
    v-stepper-step(:complete='step > 3' step='3') Select an ad format and name ad unit
    
    v-stepper-content(step='3')
      v-card.mb-12(color='grey lighten-1' height='200px')
      v-btn(color='primary') Continue
      v-btn(text='') Cancel

</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import { requestDevice } from "@/util/bluetooth"

@Component
export default class Setup extends Vue {
  step = 1

  async pairBluetooth() {
    const success = await requestDevice()

    if (success) {
      this.step = 2
    }
  }
}
</script>