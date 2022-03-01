import { db } from '@/config/firebase'
import router from '@/router'
import firebase from 'firebase/compat'
import Vue from 'vue'
import Vuex from 'vuex'
import { firebaseAction, vuexfireMutations } from 'vuexfire'

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
  }
}

export default new Vuex.Store({
  state: initialState(),
  mutations: {
    ...vuexfireMutations,
    SET_ME(state: any, me: firebase.User | null) {
      state.me = me
    },
    SET_BT_DEVICE(state: any, device: any) {
      state.btDevice = device
    },
  },
  actions: {
    logIn: async ({ commit, dispatch }, user) => {
      try {
        const provider = new firebase.auth.GoogleAuthProvider()

        const result = await firebase.auth().signInWithPopup(provider)

        const { user } = result
        const credential = result.credential as firebase.auth.OAuthCredential
        const { accessToken } = credential

        console.log(user, accessToken)

        // TODO: Save token for persistent auth
        commit('SET_ME', user)
        router.push({name: 'lamps'})
        dispatch('bindData')
      }
      catch (error) {
        console.error(error)
      }
    },
    bindData: ({ dispatch }) => {
      dispatch('bindLamps')
      dispatch('bindGroups')
    },
    unbindData: ({ dispatch }) => {
      dispatch('unbindLamps')
      dispatch('unbindGroups')
    },
    bindGroups: firebaseAction(({ bindFirebaseRef }) => {
      return bindFirebaseRef('groups', db.ref('groups'))
    }),
    bindLamps: firebaseAction(({ bindFirebaseRef }) => {
      return bindFirebaseRef('lamps', db.ref('lamps'))
    }),
    unbindGroups: firebaseAction(({ unbindFirebaseRef }) => {
      return unbindFirebaseRef('groups')
    }),
    unbindLamps: firebaseAction(({ unbindFirebaseRef }) => {
      return unbindFirebaseRef('lamps')
    }),
  },
  getters: {},
  modules: {},
})
