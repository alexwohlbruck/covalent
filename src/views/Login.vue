<template lang="pug">
  .login
    #firebaseui-auth
</template>

<script>
/*eslint no-undef: "off"*/
import firebase from 'firebase/compat/app'
import 'firebaseui/dist/firebaseui.css'
import * as firebaseui from 'firebaseui'

export default {
  name: 'Login',
  mounted: () => {
    console.log(firebaseui)
    const auth = firebase.auth()
    const ui = new firebaseui.auth.AuthUI(auth)
    const uiConfig = {
      signInSuccessUrl: '/',
      signInOptions: [firebase.auth.GoogleAuthProvider.PROVIDER_ID],
    }
    ui.start('#firebaseui-auth', uiConfig)
  },
}
</script>
