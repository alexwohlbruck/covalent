
export interface AppState {
  btDevice: null // TODO: Move to Bluetooth module
  error: {
    show: boolean
    message: string
  }
}

export const initialState = (): AppState => ({
  btDevice: null,
  error: {
    show: false,
    message: '',
  },
})
const mutations = {
  // SET_ME(state: AppState, me: any | null) {
  //   state.me = me || null
  // },

  SET_BT_DEVICE(state: AppState, device: any) {
    state.btDevice = device
  },

  SET_ERROR(state: AppState, error: string | null) {
    if (error) {
      state.error = {
        show: true,
        message: error,
      }
    }
    else {
      state.error = {
        show: false,
        message: '',
      }
    }
  }
}

export default {
  state: initialState(),
  mutations,
}