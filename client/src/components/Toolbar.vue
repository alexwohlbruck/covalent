<template lang="pug">

v-app-bar(app :color="$vuetify.breakpoint.mdAndUp ? 'transparent' : 'black'" flat)
  v-toolbar-title
    router-link.d-flex(:to="{ name: 'home' }" v-if='$route.name !== "home"')
      v-img(src='@/assets/icon.svg' width='40')
      v-img(src='@/assets/logotype.svg' height='25' width='110' style='margin: 8px 0 0 8px')

  v-spacer

  div(v-if='me')
    v-menu(
      v-model='userMenu'
      :close-on-content-click='false'
      :nudge-width='200'
    )
      template(v-slot:activator='{ on, attrs }')
        v-fade-transition
          v-avatar(
            v-show='!userMenu'
            v-bind='attrs'
            v-on='on'
            size='35px'
          )
            v-img(:src='me.picture')
      
      v-card
        v-list
          v-list-item
            v-list-item-avatar
              v-img(:src='me.picture' :alt='me.name')

            v-list-item-content
              v-list-item-title {{ me.name }}
              v-list-item-subtitle {{ me.email }}
            
            v-list-item-action(icon)
              v-icon mdi-heart
        
        v-divider
        
        v-card-actions
          v-spacer
          v-btn(@click='signOut' color='primary' text) Sign out

</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { signOut } from '@/services/auth'

@Component
export default class Toolbar extends Vue {

  userMenu = false

  get me() {
    return this.$store.getters.me
  }

  get btDevice() {
    return this.$store.state.btDevice
  }

  async signOut() {
    this.userMenu = false
    await signOut()
  }
}
</script>
