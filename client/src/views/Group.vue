<template lang="pug">
v-container.group
  .d-flex
    v-btn(icon :to="{ name: 'lamps' }")
      v-icon mdi-arrow-left

    h1.text-h5.font-weight-medium {{ group.groupId }}

  lamp-visualizer.px-15(
    v-if='myLamp'
    :state='group.state'
    :lampId='myLamp._id'
    selectedColor='#000000'
  )

  v-list(v-if='group')
    v-subheader Participants
    
    v-list-item(v-for='lamp in group.lamps' :key='lamp._id')
      v-list-item-avatar
        v-img(:src='lamp.user.picture')
      v-list-item-content
        v-list-item-title {{ lamp.user.name }}

</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { getGroup } from '@/services/group'
import { Group as IGroup } from '@/types/Group'
import LampVisualizer from '@/components/LampVisualizer.vue'

@Component({
  components: {
    LampVisualizer,
  },
})
export default class Group extends Vue {
  async mounted() {
    await getGroup(this.$route.params.id)
  }

  get me() {
    return this.$store.getters.me
  }

  get group(): IGroup {
    return this.$store.getters.group(this.$route.params.id)
  }

  get myLamp() {
    return this.group?.lamps?.find((lamp) => lamp.user?._id === this.me?._id)
  }
}
</script>