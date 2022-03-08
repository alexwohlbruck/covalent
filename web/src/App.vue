<template lang="pug">
v-app
  v-snackbar(v-model='error.show' :timeout='5000') {{ error.message }}

  toolbar
  v-main
    router-view
</template>

<script lang="ts">
import Vue from 'vue'
import Toolbar from '@/components/Toolbar.vue'
import { mapState } from 'vuex'

export default Vue.extend({
  name: 'App',

  components: {
    Toolbar,
  },

  data: (): any => ({
    device: null,
    ssid: '',
    password :'',
  }),

  computed: {
    ...mapState(['error']),
  },
})
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