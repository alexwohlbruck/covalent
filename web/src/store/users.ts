import { User } from '@/types/User'

export interface AppState {
  me: User | null
}

export const initialState = (): AppState => ({
  me: null,
})

const mutations = {
  SET_ME(state: AppState, me: any | null) {
    state.me = me || null
  },
}

export default {
  state: initialState(),
  mutations,
}