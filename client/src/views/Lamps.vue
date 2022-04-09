<template lang="pug">
v-container
  v-card.mb-4(v-for='(lamp, i) in myLamps' :key='i')
    .d-flex.flex-column.flex-sm-row.align-center.align-sm-start
      lamp-visualizer.px-15(
        :state='lamp.group ? lamp.group.state : lamp.state'
        :lampId='lamp._id'
        selectedColor='#000000'
      )
      v-card-text.d-flex.flex-column
        .d-flex
          .text-h6 {{ lamp.name }}
          v-spacer
          v-btn(icon :to="{name: 'lamp-settings', params: {id: lamp._id}}")
            v-icon mdi-cog
          
        span Group: {{ lamp.group.groupId }}
        span Access code: {{ lamp.group.accessCode }}
        v-btn(:to="{ name: 'group', params: { id: lamp.group._id } }") Open group
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