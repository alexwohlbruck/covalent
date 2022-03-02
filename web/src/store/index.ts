import { db, functions, auth } from '@/config/firebase'
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
    error: {
      show: false,
      message: '',
    },
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

    async createLamp({ dispatch }, {
      groupId, accessCode, deviceData
    }: {
      groupId: string,
      accessCode: string,
      deviceData: any
    }) {
      try {
        console.log('creating lamp')
        const createLamp = functions.httpsCallable('createLamp')
        const result = await createLamp({
          groupId,
          accessCode,
          deviceData,
        })
        console.log(result)
        router.push({name: 'lamps'})
        return result
      }
      catch (error: any) {
        dispatch('error', error?.details?.message)
      }
    },

    error: ({ commit }, error: string) => {
      console.error(error)
      commit('SET_ERROR', error)
      setTimeout(() => {
        commit('SET_ERROR', null)
      }, 5000)
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
