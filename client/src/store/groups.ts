import { Group } from '@/types/Group'
import Vue from 'vue'

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
    console.log(group)
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
  group: (state: GroupsState) => (id: string) => state.byId[id],
  groups: (state: GroupsState) => (ids: string[]) => ids.map(id => state.byId[id]),
}

export default {
  state: initialState(),
  mutations,
  getters,
}