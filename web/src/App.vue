<template lang="pug">
v-app
  v-main
    v-btn(@click='requestDevice') connect
    v-btn(@click='disconnect') disconnect
    v-btn(@click='sendWifi') send wifi
    v-text-field(v-model='ssid') ssid
    v-text-field(v-model='password') password
    router-view
</template>

<script lang="ts">
import Vue from 'vue'
import {
  BleClient,
  textToDataView,
  dataViewToText,
} from '@capacitor-community/bluetooth-le'

const NUS_UUID = '6e400001-b5a3-f393-e0a9-e50e24dcca9e' // Nordic UART Service
const RX_UUID = '6e400002-b5a3-f393-e0a9-e50e24dcca9e' // Receiver characteristic
const TX_UUID = '6e400003-b5a3-f393-e0a9-e50e24dcca9e' // Sender characteristic

export default Vue.extend({
  name: 'App',

  data: (): any => ({
    device: null,
    ssid: '',
    password :'',
  }),

  methods: {
    async disconnect() {
      console.log('TODO')
    },

    async requestDevice() {

      console.log('starting bt')

      await BleClient.initialize()

      console.log('initialized')

      const device = await BleClient.requestDevice({
        // services: [NUS_UUID],
        optionalServices: [NUS_UUID],
        name: 'mpy-uart'
      }) // TODO: Filter service to NUS
      
      this.device = device
      this.connect()
    },

    async connect() {
      console.log('Connecting to ' + this.device.name)

      await BleClient.connect(this.device.deviceId, (deviceId: string) => {
        console.log(deviceId + ' disconnected')
      })

      console.log('connected')

      const services = await BleClient.getServices(this.device.deviceId)
      console.log(services)

      // Listen for messages
      BleClient.startNotifications(
        this.device.deviceId,
        NUS_UUID, // Service
        TX_UUID, // Characteristic
        (buffer: DataView) => {
          console.log(dataViewToText(buffer))
        }
      )
    },

    async sendWifi() {
      await this.write(JSON.stringify({
        name: 'wifi',
        data: {
          ssid: this.ssid,
          password: this.password,
        },
      }))
    },

    async write(string: string) {
      await BleClient.write(
        this.device.deviceId,
        NUS_UUID,
        RX_UUID,
        textToDataView(string),
      )
    },
  },
})
</script>
