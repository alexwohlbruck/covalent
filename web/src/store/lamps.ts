import { Lamp } from '@/types/Lamp'
import Vue from 'vue'
import { RootState } from '.'

export interface LampsState {
  all: string[]
  byId: {
    [id: string]: Lamp
  }
}

export const initialState = (): LampsState => ({
  all: [],
  byId: {},
})

const getters = {
  lamp: (state: LampsState) => (id: number) => {
    return state.byId[id]
  },

  lamps: (_state: LampsState, getters: any) => (ids: string[]) => {
    return ids.map((id: string) => getters.lamp(id))
  },

  myLamps: (state: LampsState, getters: any, _rootState: RootState, rootGetters: any) => {
    return getters
      .lamps(state.all)
      .filter((lamp: Lamp) => lamp.user._id === rootGetters.me?._id)
  }
}

const mutations = {
  ADD_LAMP(state: LampsState, lamp: Lamp) {
    Vue.set(state.byId, lamp._id, lamp)
    if (!state.all.includes(lamp._id)) state.all.push(lamp._id)
  },

  REMOVE_LAMP(state: LampsState, lamp: Lamp) {
    Vue.delete(state.byId, lamp._id)
    const index = state.all.indexOf(lamp._id)
    if (index > -1) state.all.splice(index, 1)
  }
}

export default {
  state: initialState(),
  mutations,
  getters,
}