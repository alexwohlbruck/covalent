<template lang="pug">

v-container.d-flex.flex-column.align-center
  v-img(src='@/assets/logo.svg' width='500')

  google-sign-in-button.black--text(v-if='!me')
  v-btn.black--text(v-if='me' color='white' :to="{ name: 'lamps' }") Open app

</template>

<script lang="ts">
/*eslint no-undef: "off"*/
import { Vue, Component } from 'vue-property-decorator'
import { getMe } from '@/services/auth'
import GoogleSignInButton from '@/components/GoogleSignInButton.vue'
import { renderButton } from '@/components/GoogleSignInButton.vue'

@Component({
  components: {
    GoogleSignInButton,
  },
})
export default class Home extends Vue {

  get me() {
    return this.$store.getters.me
  }

  async loadMe() {
    await getMe()
    renderButton()
  }
}
</script>
