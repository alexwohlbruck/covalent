<template lang="pug">
  v-container.home

    login(v-show='!user')

    //- Header/auth info
    .d-flex.align-center(v-if='user')
      img.mr-4(:src='user.photoURL' width='50' height='50')
        
      v-list-item-content
        v-list-item-title
          span.text-subtitle-1.font-weight-bold {{user.displayName}}
        v-list-item-subtitle(v-if='userMeta.groupId') Group: {{ userMeta.groupId | kebabToTitle | capitalize }}

      v-spacer

      .d-flex.align-center
        v-btn.ml-2(v-if='isInGroup' @click='leaveGroup') Leave
        
        form.d-flex.align-center(v-else @submit.prevent='joinGroup' )
          v-text-field.ml-2(
            v-model='controls.groupId'
            outlined
            dense
            placeholder='Group ID'
            hide-details
          )
          v-btn.ml-2(type='submit' @click='joinGroup') Join
        
        v-btn.ml-2(@click='logout') Log out

    //- Lamp info
    .d-flex.flex-column.flex-sm-row
      .flex-grow-1.d-flex.flex-column.align-center
        lamp(
          v-if='group && group.userStates'
          :group='group'
          :user='user'
          :states='states'
          :selectedColor='selectedColor'
        )
          
        //- Color picker
        form(v-if='isInGroup' @submit.prevent='updateLamp')
          .d-flex.flex-column.align-center
            .d-flex
              v-slider(
                style='width: 150px'
                v-model='controls.hue'
                min='0'
                max='360'
                :color='selectedColor'
                :track-color='shiftedColor'
              )
      
      //- Users list
      v-card(v-if='isInGroup')
        v-list
          v-subheader Users in {{ userMeta.groupId | kebabToTitle | capitalize }}
          v-list-item(v-for='(user, i) in users' :key='i')
            v-list-item-avatar
              v-img(:src='user.photoURL')

            v-list-item-content
              v-list-item-title {{ user.displayName }}

</template>

<script>
import { db, functions, auth } from '@/config/firebase'
import Lamp from '@/components/Lamp.vue'
import Login from '@/views/Login.vue'

import { hslToHexString, hexStringToHsl } from '@/util'

const defaultState = () => {
  return {
    user: null,
    userMeta: null,
    group: null,
    groups: null,
    users: null,
    controls: {
      hue: 0,
    },
  }
}

export default {
  name: 'Home',
  components: {
    Login,
    Lamp,
  },
  data: defaultState,
  mounted() {
    // Get current firebase user
    auth.onAuthStateChanged((user) => {
      if (user) {
        this.user = user
        this.updateProfile({ ...user._delegate })
      } else {
        this.signOut()
      }
    })
  },

  filters: {
    kebabToTitle(value) {
      if (!value) return ''
      return value.replace(/-/g, ' ')
    },
    capitalize(value) {
      return value.charAt(0).toUpperCase() + value.slice(1)
    },
  },
  watch: {
    user: {
      handler(user) {
        if (user) {
          const groupIdRef = db.ref(`users/${user.uid}`)
          this.$rtdbBind('userMeta', groupIdRef)
        }
      },
      immediate: true,
    },
    userMeta: {
      async handler(userMeta) {
        if (userMeta) {
          const group = db.ref(`groups/${userMeta.groupId}`)
          this.$rtdbBind('group', group)
          this.$rtdbBind(
            'users',
            db.ref('users').orderByChild('groupId').equalTo(userMeta.groupId)
          )

          const snapshot = await group.once('value')
          this.controls.lamp = snapshot.val().lamp
        }
      },
      immediate: true,
    },
  },
  computed: {
    isInGroup() {
      return this.userMeta && this.userMeta.groupId
    },
    selectedColor() {
      return hslToHexString(this.controls.hue, 100, 50)
    },
    shiftedColor() {
      const hsl = hexStringToHsl(this.selectedColor)
      hsl[0] = hsl[0] + 40
      return hslToHexString(...hsl)
    },
    states() {
      console.log('state changed')
      if (!this.group) return []
      return Object.keys(this.group.userStates)
        .map((key) => this.group.userStates[key])
        .sort((a, b) => b.timestamp - a.timestamp)
    },
    groupRef() {
      if (!this.group) return null
      return db.ref(`groups/${this.group['.key']}`)
    },
  },
  methods: {
    async joinGroup() {
      const joinGroup = functions.httpsCallable('joinGroup')
      await joinGroup({
        groupId: this.controls.groupId,
      })
    },
    async leaveGroup() {
      const leaveGroup = functions.httpsCallable('leaveGroup')
      await leaveGroup()
    },
    async updateProfile(userInfo) {
      const { uid, displayName, photoURL } = userInfo
      await db.ref(`users/${uid}`).update({ uid, displayName, photoURL })
    },
    async logout() {
      await auth.signOut()
      const state = defaultState()
      Object.keys(state).forEach((key) => {
        this[key] = state[key]
      })
    },
  },
}
</script>
