<template lang="pug">
v-container
  v-card.mb-4.pa-6.red(v-for='(lamp, i) in myLamps' :key='i')
    .d-flex.flex-column.mb-4
      .text-h6 My group
      .text-subtitle-2 2 lamps
        
    v-card(light)
      v-card-text.d-flex.flex-column
        .d-flex
          .text-h5.font-weight-bold.red--text {{ lamp.name }}
          v-spacer
          v-btn(icon color='black' :to="{name: 'lamp-settings', params: {id: lamp._id}}")
            v-icon mdi-cog
      .d-flex.align-end.justify-space-between.pa-6
        lamp-visualizer.px-15(
          :state='lamp.group ? lamp.group.state : lamp.state'
          :lampId='lamp._id'
          selectedColor='#000000'
        )
        v-btn(
          color='red'
          x-large
        )
          | Send pulse
      div.color-slider
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { getMyLamps } from '@/services/lamp'
import LampVisualizer from '@/components/LampVisualizer.vue'

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

<style>
.color-slider {
  width: 100%;
  height: 3rem;
  background: linear-gradient(to right, red, #ff8000, yellow, #80ff00, lime, #00ff80, aqua, #0080ff, blue, #8000ff, fuchsia, #ff0080, red);
}
</style>