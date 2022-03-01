<template lang="pug">

v-container
  h1 Friendship lamp
  v-btn.black--text(color='white' @click='logIn') Sign in with Google

</template>

<script lang="ts">
/*eslint no-undef: "off"*/
import firebase from 'firebase/compat/app'
import 'firebaseui/dist/firebaseui.css'
import * as firebaseui from 'firebaseui'
import { mapState } from 'vuex'

export default {
  name: 'Login',
  methods: {
    logIn() {
      (this as any).$store.dispatch('logIn')
    }
  },
  computed: {
    ...mapState(['me']),
  },
}
</script>
