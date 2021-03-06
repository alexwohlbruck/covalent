import Vue from 'vue'
import { User } from '@/types/User'

export interface UsersState {
  me: string | null,
  all: string[]
  byId: {
    [id: string]: User
  }
}

export const initialState = (): UsersState => ({
  me: null,
  all: [],
  byId: {},
})

const addUser = (state: UsersState, user: User) => {
  if (!user) return
  Vue.set(state.byId, user._id, {
    ...state.byId[user._id],
    ...user,
  })
  if (!state.all.includes(user._id)) state.all.push(user._id)
}

const mutations = {
  SET_ME(state: UsersState, me: User | null) {
    if (me && me._id) {
      addUser(state, me)
    }
    state.me = me?._id || null
  },

  ADD_USER(state: UsersState, user: User) {
    addUser(state, user)
  },

  REMOVE_USER(state: UsersState, user: User) {
    Vue.delete(state.byId, user._id)
    state.all = state.all.filter(id => id !== user._id)
  },
}

const usersGetters = {
  user: (state: UsersState) => (id: string) => {
    return state.byId[id]
  },

  users: (_state: UsersState, getters: any) => (ids: string[]) => {
    return ids.map((id: string) => getters.user(id))
  },

  me: (state: UsersState, getters: any) => {
    return getters.user(state.me)
  }
}

export default {
  state: initialState(),
  mutations,
  getters: usersGetters,
}