import Vue from 'vue'
import { Group } from '@/types/Group'
import { RootState } from '.'

export interface GroupsState {
  all: string[]
  byId: {
    [id: string]: Group
  }
}

export const initialState = (): GroupsState => ({
  all: [],
  byId: {},
})

const mutations = {
  ADD_GROUP(state: GroupsState, group: Group) {
    Vue.set(state.byId, group._id, {
      ...state.byId[group._id],
      ...group,
    })
    if (!state.all.includes(group._id)) state.all.push(group._id)
  },

  REMOVE_GROUP(state: GroupsState, group: Group) {
    Vue.delete(state.byId, group._id)
    const index = state.all.indexOf(group._id)
    if (index > -1) state.all.splice(index, 1)
  },

  GROUP_STATE_CHANGED(state: GroupsState, newState: {
    groupId: string
    state: {
      colors: string[]
      active: boolean
    }
  }) {
    const group = state.byId[newState.groupId]
    if (!group) return
    group.state = {
      ...newState.state,
    }
  }
}

const getters = {
  group: (state: GroupsState, getters: any, _rootState: RootState, rootGetters: any) => (id: string) => {
    const g = state.byId[id]
    g.lamps = rootGetters.lampsByGroup(id)
    return g
  },
  groups: (state: GroupsState, getters: any) => (ids: string[]) => ids.map(id => getters.group(id)),
  myGroups: (state: GroupsState, getters: any, _rootState: RootState, _rootGetters: any) => {
    return getters
      .groups(state.all)
      // .filter((lamp: Lamp) => lamp.user?._id === rootGetters.me?._id)
  }
}

export default {
  state: initialState(),
  mutations,
  getters,
}