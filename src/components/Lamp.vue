<template lang="pug">
div
  span.flex-shrink-1.lamp(
    :style='visualizerStyle'
    :class='{pulsing: incomingMessage, active}'
    @mousedown='updateLamp(true)'
    @touchstart='updateLamp(true)'
    @mouseup='updateLamp(false)'
    @touchend='updateLamp(false)'
  )
</template>

<script>
import { db } from '@/config/firebase'
import { hslToHexString, hexStringToHsl } from '@/util'

let timeout

export default {
  name: 'lamp',
  props: {
    group: Object,
    user: Object,
    states: Array,
    selectedColor: String,
  },
  data: () => ({
    active: false,
  }),
  watch: {
    states() {
      this.active = true
      clearTimeout(timeout)
      timeout = setTimeout(() => {
        this.active = false
      }, 10000)
    },
  },
  computed: {
    myStateRef() {
      if (!this.group) return null
      return db.ref(`groups/${this.group['.key']}/userStates/${this.user.uid}`)
    },
    incomingMessage() {
      const userStates = this.group.userStates
      const colors = Object.keys(userStates)
        .filter((uid) => uid !== this.user.uid)
        .map((key) => userStates[key])
        .filter((state) => state.touching)
        .sort((a, b) => a.timestamp - b.timestamp)
        .map((state) => state.color)

      return colors.length != 0
    },
    visualizerStyle() {
      let colors = this.states
        .filter((state) => state.touching)
        .map((state) => state.color)

      if (colors.length === 0) colors = [this.states[0]?.color || '#000000']

      const firstColor = colors[0]

      if (colors.length == 1) {
        // Add a second color that is slightly shifted
        const hsl = hexStringToHsl(firstColor)
        hsl[0] = hsl[0] + 40
        const shiftedColor = hslToHexString(...hsl)
        colors.push(shiftedColor)
      }

      return {
        'box-shadow': `0px 0px 50px 30px ${firstColor}`,
        background: `black linear-gradient(135deg, ${colors.join(',')})`,
      }
    },
  },
  methods: {
    async updateLamp(touching) {
      const color = this.selectedColor
      await this.myStateRef.update({
        touching,
        color,
        timestamp: Date.now(),
      })
    },
  },
}
</script>

<style lang="scss">
@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.7;
  }
  20% {
    transform: scale(1.1);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 0.7;
  }
}

$size: 200px;

.lamp {
  display: block;
  margin: 50px 0;
  width: $size;
  height: $size;
  border-radius: 50%;
  transition: all 1s ease;
  opacity: 0.2;

  &.active {
    opacity: 1;
  }

  &.pulsing {
    animation: pulse 1s ease-in-out infinite;
  }
}
</style>
