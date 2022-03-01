<template lang="pug">

v-container
  v-stepper(v-model='step' vertical)

    //- Bluetooth pairing
    v-stepper-step(:complete='step > 1' step='1')
      | Connect to your lamp
      small.success--text.font-weight-bold.mt-1(v-if='btDevice') {{ btDevice.name }}

    v-stepper-content(step='1')
      v-sheet(color='transparent')
        v-card-text Allow Bluetooth access and then connect to your lamp in the devices list.
        v-card-text
          v-btn(@click='pairBluetooth' color='blue darken-1') Pair with bluetooth

    //- Wifi config
    v-stepper-step(:complete='step > 2' step='2')
      | Connect your lamp to Wifi
      small.success--text.font-weight-bold.mt-1(v-if='connectedNetwork') {{ connectedNetwork.ssid }}

    v-stepper-content(step='2')
      .d-flex.flex-column(v-if='availableNetworks.length || loadingAvailableNetworks')
        v-progress-circular(v-if='loadingAvailableNetworks' indeterminate)

        div(v-else)
          v-sheet(color='transparent')
            v-card-text Select your Wifi network and enter the password
          
          v-list
            v-list-item-group(v-model='selectedNetworkIndex')
              v-list-item(
                v-for='(network, i) in availableNetworks'
                :key='i'
              )
                v-list-item-content
                  v-list-item-title {{ network.ssid }}

          .mt-4(v-if='networkSelected')
            v-text-field(
              autofocus
              outlined
              label='Wifi password'
              v-model='password'
            )

            v-btn(
              @click='connectToNetwork'
              color='blue darken-1'
              :loading='connectingToNetwork'
            ) Connect

    //- Group config
    v-stepper-step(:complete='step > 3' step='3') Add your lamp to a group
    
    v-stepper-content(step='3')
      v-card.mb-12(color='grey lighten-1' height='200px')
      v-btn(color='primary') Continue
      v-btn(text='') Cancel

</template>

<script lang="ts">

import { Component, Vue, Watch } from 'vue-property-decorator'
import { Network } from '@/store'
import {
  emitter,
  requestDevice,
  requestNetworks,
  connectToNetwork,
  AVAILABLE_NETWORKS,
  CONNECTION_SUCCESS,
  CONNECTION_FAILURE,
 } from "@/util/bluetooth"

@Component
export default class Setup extends Vue {
  
  step = 1
  password = ''
  selectedNetworkIndex = -1
  availableNetworks: Network[] = []
  loadingAvailableNetworks = false
  connectingToNetwork = false
  connectedNetwork: Network | null = null

  mounted() {
    emitter.on(AVAILABLE_NETWORKS, (payload: any) => {
      this.availableNetworks = payload.networks
      this.loadingAvailableNetworks = false
    })

    emitter.on(CONNECTION_SUCCESS, (payload: any) => {
      this.connectingToNetwork = false
      this.connectedNetwork = payload
      this.step = 3
    })

    emitter.on(CONNECTION_FAILURE, (payload: any) => {
      this.connectingToNetwork = false
      this.connectedNetwork = null
    })
  }

  @Watch('step')
  async onStepChange(step: number) {
    switch (step) {
      case 2:
        await this.requestNetworks()
        break
    }
  }

  async pairBluetooth() {
    const success = await requestDevice()

    if (success) {
      this.step = 2
    }
  }

  get btDevice() {
    return this.$store.state.btDevice
  }

  async requestNetworks() {
    this.loadingAvailableNetworks = true
    await requestNetworks()
  }

  async connectToNetwork() {
    if (!this.selectedNetwork) return
    this.connectingToNetwork = true
    await connectToNetwork(this.selectedNetwork.ssid, this.password)
  }

  get selectedNetwork() {
    if (!this.networkSelected) return null
    return this.availableNetworks[this.selectedNetworkIndex]
  }

  get networkSelected() {
    return this.selectedNetworkIndex !== -1
  }
}
</script>