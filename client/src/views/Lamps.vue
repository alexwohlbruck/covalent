<template lang="pug">
v-container

  .d-flex.flex-column.align-center(v-if='!(myLamps && myLamps.length)' style='padding-top: calc(50vh - 260px)')
    p.text-h6 You have no lamps.
    v-img.mt-5.mb-10(src='@/assets/undraw_signal_searching.svg' width='300')


  .d-flex.flex-column.align-center(v-else)
    v-card.lamp-card.mb-4.pa-6(
      v-for='(group, groupId) in groups'
      :key='groupId'
      :style='`background: ${gradient(group.group.state)}; width: 600px; max-width: 100%; box-shadow: ${shadow(group.group.state)};`'
    )
      .d-flex.flex-column.mb-4
        .text-h6 {{ group.group.groupId }}
        .text-subtitle-2 {{ group.lamps.length }} {{ group.lamps.length === 1 ? 'lamp' : 'lamps' }}

      lamp(v-for='lamp in group.lamps' :key='lamp._id' :lamp='lamp')
    
  .d-flex.justify-center
    v-btn.ml-4(
      text
      :to="{name: 'setup'}"
    )
      v-icon(left) mdi-plus
      span Add lamp

</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { getMyLamps } from '@/services/lamp'
import Lamp from '@/components/Lamp.vue'
import { colorShadow, gradientFromHue } from '@/util'
import { hexStringToHsl } from '@/util'

@Component({
  components: {
    Lamp,
  },
})
export default class Lamps extends Vue {

  get myLamps() {
    return this.$store.getters.myLamps
  }

  get groups() {
    // Return unqiue groups with their respective lamps in a list
    return this.myLamps.reduce((acc: any, lamp: any) => {
      if (lamp.group) {
        if (!acc[lamp.group._id]) {
          acc[lamp.group._id] = {
            group: lamp.group,
            lamps: [lamp],
          }
        } else {
          acc[lamp.group._id].lamps.push(lamp)
        }
      }
      return acc
    }, {})
  }

  shadow(state: any) {
    const hue = hexStringToHsl(state.colors[0])[0]
    return colorShadow(hue)
  }

  async mounted() {
    await getMyLamps()
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
