<template lang="pug">

v-container
  google-sign-in-button
</template>

<script lang="ts">
/*eslint no-undef: "off"*/
import { Vue, Component } from 'vue-property-decorator'
import { mapState } from 'vuex'
import { getMe } from '@/services/auth'
import GoogleSignInButton from '@/components/GoogleSignInButton.vue'

@Component({
  components: {
    GoogleSignInButton,
  },
})
export default class Login extends Vue {

  get me() {
    return this.$store.state.me
  }

  loadMe() {
    getMe()
  }
}
</script>
