import Vue from 'vue'
import Vuex, { StoreOptions } from 'vuex'

import * as app from './app'
import * as lamps from './lamps'
import * as groups from './groups'
import * as users from './users'

Vue.use(Vuex)

export interface RootState {
  app: app.AppState
  lamps: lamps.LampsState
  groups: groups.GroupsState
  users: users.UsersState
}
export interface Network {
  ssid: string
}

const storeConfig: StoreOptions<RootState> = {
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
}

export default new Vuex.Store(storeConfig)
