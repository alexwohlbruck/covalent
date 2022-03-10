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
    RESET_STATE(state) {
      Object.assign(state.app, app.initialState())
      Object.assign(state.lamps, lamps.initialState())
      Object.assign(state.groups, groups.initialState())
      Object.assign(state.users, users.initialState())
    },
  },
  modules: {
    app: app.default,
    lamps: lamps.default,
    groups: groups.default,
    users: users.default,
  },
}

export default new Vuex.Store(storeConfig)
