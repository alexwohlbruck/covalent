<template lang="pug">
v-container
  h1.text-h4 My lamps
  v-card(v-for='(lamp, i) in lamps' :key='i')
    pre {{ lamp }}
</template>

<script lang="ts">
import { mapState } from 'vuex'

export default {
  name: 'lamps',
  computed: {
    ...mapState(['lamps']),
  },
}
</script>