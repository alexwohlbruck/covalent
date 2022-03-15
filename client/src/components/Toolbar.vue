<template lang="pug">

v-app-bar(app)
  v-toolbar-title Covalent
  v-spacer

  v-btn(
    v-if='btDevice'
    text
    color='blue darken-1'
  )
    v-icon(left) mdi-bluetooth-connect
    | {{btDevice.name}}

  v-btn(
    v-else
    text
    :to="{name: 'setup'}"
  ) Pair lamp

  v-btn(
    v-if='me'
    text
    @click='signOut'
  ) Log out

  v-btn(
    v-else
    text
    :to="{ name: 'login' }"
  ) Log in

  div(v-if='me')
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
    return this.$store.getters.me
  }

  get btDevice() {
    return this.$store.state.btDevice
  }

  async signOut() {
    await signOut()
  }
}
</script>
