import { Lamp } from '@/types/Lamp'
import Vue from 'vue'
import { RootState } from '.'
import UsersStore from './users'
import GroupsStore from './groups'
const { mutations: usersMutations, state: usersState } = UsersStore
const { mutations: groupsMutations, state: groupsState } = GroupsStore

export interface LampsState {
  all: string[]
  byId: {
    [id: string]: Lamp
  },
}

export const initialState = (): LampsState => ({
  all: [],
  byId: {},
})

const lampsGetters = {
  lamp: (state: LampsState, getters: any) => (id: number) => {
    const lamp = {...state.byId[id]}

    // Denormalize data
    if (lamp.groupId) {
      lamp.group = getters.group(lamp.groupId)
      delete lamp.groupId
    }

    if (lamp.userId) {
      lamp.user = getters.user(lamp.userId)
      delete lamp.userId
    }

    return lamp
  },

  lamps: (_state: LampsState, getters: any) => (ids: string[]) => {
    return ids.map((id: string) => getters.lamp(id))
  },

  myLamps: (state: LampsState, getters: any, _rootState: RootState, rootGetters: any) => {
    return getters
      .lamps(state.all)
      // .filter((lamp: Lamp) => lamp.user?._id === rootGetters.me?._id)
  }
}

const mutations = {
  ADD_LAMP(state: LampsState, lamp: Lamp) {
    if (lamp.user) {
      UsersStore.mutations.ADD_USER(UsersStore.state, lamp.user)
      lamp.userId = lamp.user._id
      delete lamp.user
    }
    if (lamp.group) {
      GroupsStore.mutations.ADD_GROUP(GroupsStore.state, lamp.group)
      lamp.groupId = lamp.group._id
      delete lamp.group
    }

    Vue.set(state.byId, lamp._id, {
      ...state.byId[lamp._id],
      ...lamp,
    })
    if (!state.all.includes(lamp._id)) state.all.push(lamp._id)
  },

  REMOVE_LAMP(state: LampsState, lamp: Lamp | { _id: string }) {
    Vue.delete(state.byId, lamp._id)
    const index = state.all.indexOf(lamp._id)
    if (index > -1) state.all.splice(index, 1)
  }
}

export default {
  state: initialState(),
  mutations,
  getters: lampsGetters,
}