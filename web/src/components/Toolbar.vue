<template lang="pug">

v-app-bar(app)
  v-toolbar-title Friendship lamp
  v-spacer

  v-btn(
    v-if='btDevice'
    text
    color='blue darken-1'
  )
    v-icon(left) mdi-bluetooth-connect
    | Friendship lamp

  v-btn(
    v-else
    text
    :to="{name: 'setup'}"
  ) Pair lamp

  div(v-if='me')
    v-btn(
      text
      @click='signOut'
      color='red darken-1'
    ) Sign out

    span.text-body-2.mr-4.font-weight-bold {{ me.name }}
    v-avatar(size='40px')
      v-img(:src='me.picture')
    

</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { signOut } from '@/services/auth'

@Component
export default class Toolbar extends Vue {
  get me() {
    return this.$store.state.me
  }

  get btDevice() {
    return this.$store.state.btDevice
  }

  async signOut() {
    await signOut()
  }
}
</script>
