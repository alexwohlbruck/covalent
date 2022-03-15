import Vue from 'vue'
import { Store } from 'vuex'

export interface SocketState {
  isConnected: boolean
  message: string
  reconnectError: boolean
}

export const initialState = (): SocketState => ({
  isConnected: false,
  message: '',
  reconnectError: false,
})

const mutations = {
  SOCKET_ONOPEN (state: SocketState, event: any)  {
    Vue.prototype.$socket = event.currentTarget
    state.isConnected = true
  },

  SOCKET_ONCLOSE (state: SocketState, event: any)  {
    state.isConnected = false
  },

  SOCKET_ONERROR (state: SocketState, event: any)  {
    console.error(state, event)
  },

  // default handler called for all methods
  SOCKET_ONMESSAGE (state: SocketState, message: any)  {
    state.message = message
  },

  // mutations for reconnect methods
  SOCKET_RECONNECT(state: SocketState, count: any) {
    console.info(state, count)
  },

  SOCKET_RECONNECT_ERROR(state: SocketState) {
    state.reconnectError = true
  },
}

const getters = {
}

export default {
  state: initialState(),
  mutations,
  getters,
}