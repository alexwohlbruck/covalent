<template lang="pug">

v-container
  v-btn.mb-3(icon @click='$router.back()')
    v-icon mdi-arrow-left

  v-card(flat outlined)
    v-stepper(v-model='step' vertical style='background: none;')

      //- Bluetooth pairing
      v-stepper-step(:complete='step > 1' step='1')
        | Connect to your lamp
        small.success--text.font-weight-bold.mt-1(v-if='btDevice') {{ btDevice.name }}

      v-stepper-content(step='1')
        v-sheet(color='transparent')
          v-card-text
            p Allow Bluetooth access and then connect to your lamp in the devices list.
            p.mb-0.font-weight-bold *Firefox, Safari, and iOS devices are not yet supported.
          v-card-text
            v-btn(@click='pairBluetooth' color='blue darken-1')
              v-icon(left) mdi-bluetooth-connect
              | Pair with bluetooth

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
            
            v-card
              v-list
                v-list-item-group(v-model='selectedNetworkIndex')
                  v-list-item(
                    v-for='(network, i) in availableNetworks'
                    :key='i'
                  )
                    v-list-item-content
                      v-list-item-title {{ network.ssid }}
                    
                    v-list-item-action
                      v-btn(icon)
                        v-icon {{ wifiStrengthIcon(network.rssi) }}

            .mt-4(v-if='networkSelected')
              v-text-field(
                autofocus
                outlined
                label='Wifi password'
                v-model='password'
              )

              v-btn.black--text(
                @click='connectToNetwork'
                color='primary'
                :loading='connectingToNetwork'
              ) Connect

      //- Group config
      v-stepper-step(:complete='step > 3' step='3') Add your lamp to a group
      
      v-stepper-content(step='3')
        v-form.d-flex.flex-column.gap-sm(ref='groupForm' @submit.prevent='createLamp')

          v-text-field(
            v-model='name'
            label='Lamp name'
            outlined
            dense 
            hide-details
            placeholder='My lamp'
          )

          v-radio-group(v-model='groupMethod')
            v-radio(value='new' label='Create new group')
            v-radio(value='existing' label='Add to existing group')

          v-text-field(
            v-model='groupId'
            label='Group ID'
            outlined
            dense
            hide-details
            :placeholder='groupMethod == "new" ? "Make up a unique name for your group" : ""'
          )
          v-text-field(
            v-if='groupMethod == "existing"'
            v-model='accessCode'
            label='Access code'
            outlined
            dense
            hide-details
          )

        .mt-4
          v-btn.black--text(color='primary' type='submit' @click='createLamp') Continue
          v-btn(text) Cancel

</template>

<script lang="ts">

import { Component, Vue, Watch } from 'vue-property-decorator'
import { Network } from '@/store'
import { showError } from '@/services/app'
import { createLamp } from '@/services/lamp'
import {
  emitter,
  requestDevice,
  requestNetworks,
  connectToNetwork,
  setLampId,
  DEVICE_DATA,
  AVAILABLE_NETWORKS,
  CONNECTION_SUCCESS,
  CONNECTION_FAILURE,
 } from "@/services/bluetooth"

@Component
export default class Setup extends Vue {
  
  deviceData: any = null

  step = 1
  password = ''
  selectedNetworkIndex = -1
  availableNetworks: Network[] = [{ssid: 'test', rssi: 1}, {ssid: 'test2', rssi: 2}]
  loadingAvailableNetworks = false
  connectingToNetwork = false
  connectedNetwork: Network | null = null

  name = ''
  groupMethod = 'new'
  groupId = ''
  accessCode = ''

  mounted() {

    emitter.on(DEVICE_DATA, (payload: any) => {
      this.deviceData = payload
    })

    emitter.on(AVAILABLE_NETWORKS, (payload: any) => {
      this.loadingAvailableNetworks = false
      this.availableNetworks = payload.networks
    })

    emitter.on(CONNECTION_SUCCESS, (payload: any) => {
      this.connectingToNetwork = false
      this.connectedNetwork = payload
      this.step = 3
    })

    emitter.on(CONNECTION_FAILURE, (payload: any) => {
      this.connectingToNetwork = false
      this.connectedNetwork = null
      showError("Couldn't connect to wifi network.")
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

  wifiStrengthIcon(dbm: number) {
    if (dbm > -60) {
      return 'mdi-wifi-strength-4'
    }
    if (dbm > -70) {
      return 'mdi-wifi-strength-3'
    }
    if (dbm > -80) {
      return 'mdi-wifi-strength-2'
    }
    return 'mdi-wifi-strength-1'
  }

  get selectedNetwork() {
    if (!this.networkSelected) return null
    return this.availableNetworks[this.selectedNetworkIndex]
  }

  get networkSelected() {
    return this.selectedNetworkIndex !== -1
  }

  async connectToNetwork() {
    if (!this.selectedNetwork) return
    this.connectingToNetwork = true
    await connectToNetwork(this.selectedNetwork.ssid, this.password)
  }

  async createLamp() {
    const requestBody: any = {
      groupId: this.groupId,
      deviceData: this.deviceData,
    }
    if (this.name.length) {
      requestBody.name = this.name
    }
    if (this.groupMethod === 'existing') {
      requestBody.accessCode = this.accessCode
    }

    const lamp = await createLamp(requestBody)

    if (lamp) setLampId(lamp._id)
  }
}
</script>

<style lang="scss">
  .v-stepper__step__step.primary {
    color: #000 !important;

    i {
      color: #000 !important;
    }
  }
</style>