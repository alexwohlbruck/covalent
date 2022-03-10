<template lang="pug">
v-container
  h1.text-h4 My lamps
  v-card(v-for='(lamp, i) in myLamps' :key='i').d-flex
    lamp-visualizer.px-15(
      :lamp='lamp'
      selectedColor='#000000'
    )
    v-card-text.d-flex.flex-column
      pre {{ lamp.state }}
      span {{ lamp.group.groupId }}
      span Access code: {{ lamp.group.accessCode }}
      span Owned by: {{ lamp.user.name }}
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { getMyLamps } from '@/services/lamp'
import LampVisualizer from '@/components/Lamp.vue'

@Component({
  components: {
    LampVisualizer,
  },
})
export default class Lamps extends Vue {

  get myLamps() {
    return this.$store.getters.myLamps
  }

  async mounted() {
    await getMyLamps()
  }
}
</script>