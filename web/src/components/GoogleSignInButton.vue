<template lang="pug">
#buttonDiv
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'

function renderButton() {
  if (!window?.google?.accounts?.id) {
    return setTimeout(renderButton, 100)
  }

  window.google.accounts.id.renderButton(
    document.getElementById('buttonDiv'),
    { theme: 'outline', size: 'large' }
  )
}
window.addEventListener('load', renderButton)

@Component
export default class GoogleSignInButton extends Vue {
  mounted() {
    renderButton()
  }
}
</script>