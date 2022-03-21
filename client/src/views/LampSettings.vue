<template lang="pug">
pre Lamp settings {{$route.params.id}}
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'

@Component
export default class LampSettings extends Vue {
  
}
</script>