<template lang="pug">
v-app
  v-snackbar(v-model='error.show' :timeout='5000') {{ error.message }}

  toolbar
  v-main
    router-view
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import Toolbar from '@/components/Toolbar.vue'

@Component({
  components: {
    Toolbar,
  },
})
export default class App extends Vue {

  device = null
  ssid = ''
  password = ''

  get error() {
    return this.$store.state.app.error
  }
}
</script>

<style>
  .gap-sm {
    gap: 8px;
  }
  .gap-md {
    gap: 16px;
  }
  .gap-lg {
    gap: 24px;
  }
  .gap-xl {
    gap: 32px;
  }
</style>