<template lang="pug">
v-container

  .d-flex.flex-column.align-center(v-if='!(myGroups && myGroups.length)' style='padding-top: calc(50vh - 260px)')
    p.text-h6 You have no lamps.
    v-img.mt-5.mb-10(src='@/assets/undraw_signal_searching.svg' width='300')


  .d-flex.flex-column.align-center(v-else)
    v-card.lamp-card.mb-4.pa-6.small-container(
      v-for='(group, groupId) in myGroups'
      :key='groupId'
      :style='`background: ${gradient(group.state)}; box-shadow: ${shadow(group.state)};`'
    )
      .d-flex.flex-column.mb-4
        .text-h6 {{ group.groupId }}
        .text-subtitle-2
          | {{ group.lamps.length }} {{ group.lamps.length === 1 ? 'lamp' : 'lamps' }}
          | - {{ group.accessCode }}

      .d-flex.flex-column(style='gap: 1.5em;')
        lamp(v-for='lamp in group.lamps' :key='lamp._id' :lamp='lamp' :state='group.state')
    
  .d-flex.justify-center
    v-btn.ml-4(
      text
      :to="{name: 'setup'}"
      outlined
    )
      v-icon(left) mdi-plus
      span Add lamp

</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { getMyGroups } from '@/services/group'
import Lamp from '@/components/Lamp.vue'
import { colorShadow, gradientFromHue } from '@/util'
import { hexStringToHsl } from '@/util'

@Component({
  components: {
    Lamp,
  },
})
export default class Lamps extends Vue {

  async mounted() {
    await getMyGroups()
  }

  get myGroups() {
    return this.$store.getters.myGroups
  }

  shadow(state: any) {
    const hue = hexStringToHsl(state.colors[0])[0]
    return colorShadow(hue)
  }

  gradient(group: any) {
    if (!group?.colors) return 'black'

    if (group.colors.length == 1) {
      const hue = hexStringToHsl(group.colors[0])[0]
      return gradientFromHue(hue)
    }

    else {
      return `linear-gradient(to right, ${group.colors.join(', ')})`
    }
  }
}
</script>


<style lang="scss">
.small-container {
  width: 600px;
  max-width: 100%;
}
</style>