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
  ADD_GROUP(state: GroupsState, Group: Group) {
    Vue.set(state.byId, Group._id, Group)
    if (!state.all.includes(Group._id)) state.all.push(Group._id)
  },

  REMOVE_GROUP(state: GroupsState, Group: Group) {
    Vue.delete(state.byId, Group._id)
    const index = state.all.indexOf(Group._id)
    if (index > -1) state.all.splice(index, 1)
  }
}

export default {
  state: initialState(),
  mutations,
}