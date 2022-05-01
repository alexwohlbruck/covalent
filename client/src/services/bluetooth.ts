import {
  BleClient,
  textToDataView,
  dataViewToText,
} from '@capacitor-community/bluetooth-le'
import store from '@/store'
import mitt from 'mitt'
import { showError } from '@/services/app'

const NUS_UUID = '6e400001-b5a3-f393-e0a9-e50e24dcca9e' // Nordic UART Service
const RX_UUID = '6e400002-b5a3-f393-e0a9-e50e24dcca9e' // Receiver characteristic
const TX_UUID = '6e400003-b5a3-f393-e0a9-e50e24dcca9e' // Sender characteristic

// RX Messages
export const REQUEST_NETWORKS = 'REQUEST_NETWORKS'
export const CONNECT_NETWORK = 'CONNECT_NETWORK'
export const SET_LAMP_ID = 'SET_LAMP_ID'

// TX Messages
export const DEVICE_DATA = 'DEVICE_DATA'
export const AVAILABLE_NETWORKS = 'AVAILABLE_NETWORKS'
export const CONNECTION_SUCCESS = 'CONNECTION_SUCCESS'
export const CONNECTION_FAILURE = 'CONNECTION_FAILURE'
export const ERROR = 'ERROR'

interface Payload {
  name: string,
  data: any,
}

export const emitter = mitt()

export async function requestDevice() {
  try {
    await BleClient.initialize()

    const device = await BleClient.requestDevice({
      // services: [NUS_UUID],
      optionalServices: [NUS_UUID],
      name: 'Friendship Lamp'
    }) // TODO: Filter service to NUS

    return await connect(device)

  }
  catch (error) {
    console.error(error)
    return false
  }
}

export async function connect(device: any) {
  try {
    await BleClient.connect(device.deviceId, disconnected)

    store.commit('SET_BT_DEVICE', device)

    // Listen for messages
    BleClient.startNotifications(
      device.deviceId,
      NUS_UUID, // Service
      TX_UUID, // Characteristic
      (buffer: DataView) => {
        const str = dataViewToText(buffer)
        console.log('Received:', str)
        const payload = JSON.parse(str)
        onMessage(payload)
      }
    )

    return true
  }
  catch (error) {
    console.error(error)
    return false
  }
}

// TODO: Device disconnected handler
export async function disconnected(deviceId: string) {
  console.log(deviceId + ' disconnected')

  BleClient.stopNotifications(deviceId, NUS_UUID, TX_UUID)
  store.commit('SET_BT_DEVICE', null)
}

// Message received payload
export function onMessage(payload: Payload) {
  const { name, data } = payload
  console.log('Received BT message:', name, data)
  emitter.emit(name, data)

  switch (name) {
    case ERROR: {
      showError(data.message)
    }
  }
}

export async function sendMessage(payload: Payload) {
  const device = store.state.app.btDevice

  if (!device) return

  await BleClient.write(
    device.deviceId,
    NUS_UUID,
    RX_UUID,
    textToDataView(JSON.stringify(payload)),
  )
}

export async function requestNetworks() {
  await sendMessage({
    name: REQUEST_NETWORKS,
    data: {},
  })
}

export async function connectToNetwork(ssid: string, password: string) {
  await sendMessage({
    name: CONNECT_NETWORK,
    data: {
      ssid,
      password,
    },
  })
}

export async function setLampId(lampId: string) {
  await sendMessage({
    name: SET_LAMP_ID,
    data: {
      lampId,
    },
  })
}