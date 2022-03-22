<template lang="pug">
v-container
  pre {{ lamp }}

  //- Lamp name
  v-text-field(
    v-model='name'
    label='Lamp name'
    outlined
    dense 
    hide-details
    placeholder='My lamp'
  )

  //- Night mode sensitivity

  //- Touch panel sensitivity

  //- Reading light color temp

  //- Delete lamp
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { getLamp } from '@/services/lamp'

@Component
export default class LampSettings extends Vue {
  
  async mounted() {
    await getLamp(this.$route.params.id)
  }

  get lamp() {
    return this.$store.getters.lamp(this.$route.params.id)
  }

}
</script>