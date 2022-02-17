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

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator'
import { db, functions, auth } from '@/config/firebase'
import Lamp from '@/components/Lamp.vue'
import Login from '@/views/Login.vue'

import { hslToHexString, hexStringToHsl } from '@/util'

type User = any

type UserMeta = {
  '.key': string
  displayName: string
  groupId: string
  photoURL: string
  uid: string
}

type Group = {
  '.key': string
  accessCode: string
  createdAt: number
  userStates: {
    [uid: string]: {
      color: string
      timestamp: number
      touching: boolean
    }
  }
}

@Component({
  components: {
    Login,
    Lamp,
  },
  filters: {
    kebabToTitle(value: string): string {
      if (!value) return ''
      return value.replace(/-/g, ' ')
    },

    capitalize(value: string): string {
      return value.charAt(0).toUpperCase() + value.slice(1)
    },
  },
})
export default class Home extends Vue {
  user: User | null = null
  userMeta: UserMeta | null = null
  group: Group | null = null
  controls = {
    groupId: '',
    hue: 0,
    lamp: null,
  }

  mounted(): void {
    // Get current firebase user
    auth.onAuthStateChanged((user: User) => {
      if (user) {
        this.user = user
        this.updateProfile({ ...user._delegate })
      } else {
        this.logout()
      }
    })
  }

  @Watch('user')
  userChanged(user: User): void {
    if (user) {
      const groupIdRef = db.ref(`users/${user.uid}`)
      this.$rtdbBind('userMeta', groupIdRef)
    }
  }

  @Watch('userMeta')
  async userMetaChanged(userMeta: UserMeta): Promise<void> {
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
  }

  get isInGroup(): boolean {
    return !!this.userMeta && !!this.userMeta.groupId
  }

  get selectedColor(): string {
    return hslToHexString(this.controls.hue, 100, 50)
  }

  get shiftedColor(): string {
    const hsl = hexStringToHsl(this.selectedColor)
    hsl[0] = hsl[0] + 40
    return hslToHexString(...hsl)
  }

  get states(): any[] {
    console.log('state changed')
    if (!this.group) return []
    return Object.keys(this.group.userStates)
      .map((key) => this.group?.userStates[key])
      .sort((a, b) => {
        return a && b ? b.timestamp - a.timestamp : 0
      })
  }

  get groupRef(): any {
    if (!this.group) return null
    return db.ref(`groups/${this.group['.key']}`)
  }

  async joinGroup(): Promise<void> {
    const joinGroup = functions.httpsCallable('joinGroup')
    await joinGroup({
      groupId: this.controls.groupId,
    })
  }

  async leaveGroup(): Promise<void> {
    const leaveGroup = functions.httpsCallable('leaveGroup')
    await leaveGroup()
  }

  async updateProfile(userInfo: UserMeta): Promise<void> {
    const { uid, displayName, photoURL } = userInfo
    await db.ref(`users/${uid}`).update({ uid, displayName, photoURL })
  }

  async logout(): Promise<void> {
    await auth.signOut()

    this.user = null
    this.userMeta = null
    this.group = null
    this.controls = {
      groupId: '',
      hue: 0,
      lamp: null,
    }
  }
}
</script>
