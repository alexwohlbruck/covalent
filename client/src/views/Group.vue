<template lang="pug">
v-container.group
  .d-flex.align-center
    v-btn.mr-2(icon :to="{ name: 'lamps' }")
      v-icon mdi-arrow-left

    .d-flex.flex-column
      h1.text-h5.font-weight-medium {{ group.groupId }}
      h6.text-caption Access code: {{ group.accessCode }}


  lamp-visualizer.px-15(
    v-if='myLamp'
    :state='group.state'
    :lampId='myLamp._id'
    selectedColor='#000000'
  )

  v-list(v-if='group')
    v-subheader Group members
    
    v-list-item(v-for='member in members' :key='member._id')
      v-list-item-avatar
        v-img(:src='member.picture')
      v-list-item-content
        v-list-item-title {{ member.name }}

      v-list-item-action
        p.text-body-2
          span(v-for='lamp in member.lamps' :key='lamp._id') {{ lamp.name }}

</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { getGroup } from '@/services/group'
import { Group as IGroup } from '@/types/Group'
import { User } from '@/types/User'
import { Lamp } from '@/types/Lamp'
import LampVisualizer from '@/components/LampVisualizer.vue'

interface Member extends User {
  lamps: Lamp[]
}

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

  get members() {
    // Collate group members into a unique list with their lamps in a list
    const members = new Map<string, Member>()

    this.group?.lamps?.forEach((lamp) => {
      const user: User = lamp.user as User
      const uid = user?._id
      if (!uid) return

      if (members.has(uid)) {
        members.get(uid)?.lamps.push(lamp)
      } else {
        members.set(uid, {
          lamps: [lamp],
          ...user,
        })
      }
    })

    return [...members.values()]
  }
}
</script>