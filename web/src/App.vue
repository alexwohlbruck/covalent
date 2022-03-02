<template lang="pug">
v-app
  v-snackbar(v-model='error.show' :timeout='5000') {{ error.message }}

  toolbar
  v-main
    //- v-btn(@click='requestDevice') connect
    //- v-btn(@click='disconnect') disconnect
    //- v-btn(@click='sendWifi') send wifi
    //- v-text-field(v-model='ssid') ssid
    //- v-text-field(v-model='password') password
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

  mounted() {
    this.$store.dispatch('bindData')
  },

  data: (): any => ({
    device: null,
    ssid: '',
    password :'',
  }),

  methods: {
    async disconnect() {
      console.log('TODO')
    },
  },

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