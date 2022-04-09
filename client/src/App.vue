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
.v-card {
  border-radius: 2rem !important;
  background: linear-gradient(#ffffff, #e8e8e8);
}
.v-card.red {
  background: linear-gradient(hsl(303, 100%, 50%),hsl(0, 100%, 50%),hsl(25, 100%, 50%)) no-repeat center center fixed;
}
</style>