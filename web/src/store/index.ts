import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)


export interface Network {
  ssid: string
}

const initialState = () => {
  return {
    me: null,
    lamps: [],
    groups: [],
    btDevice: null,
    error: {
      show: false,
      message: '',
    },
  }
}

export default new Vuex.Store({
  state: initialState(),
  mutations: {
    SET_ME(state: any, me: any | null) {
      state.me = me || null
    },
    SET_BT_DEVICE(state: any, device: any) {
      state.btDevice = device
    },
    SET_ERROR(state: any, error: string) {
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
  },
  actions: {

    async createLamp({ dispatch }, {
      groupId, accessCode, deviceData
    }: {
      groupId: string,
      accessCode: string,
      deviceData: any
    }) {
      try {
        // TODO
        // const result = await createLamp({
        //   groupId,
        //   accessCode,
        //   deviceData,
        // })
        // router.push({name: 'lamps'})
        // return result
      }
      catch (error: any) {
        dispatch('error', error?.details?.message)
      }
    },

    error: ({ commit }, error: string) => {
      console.error(error)
      commit('SET_ERROR', error)
      setTimeout(() => {
        commit('SET_ERROR', null)
      }, 5000)
    },
  },
  getters: {},
  modules: {},
})
