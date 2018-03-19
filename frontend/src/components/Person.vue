
<template>
    <v-avatar
	:size="52"
	class="grey lighten-4"
	v-on:mouseover="mouseOver"
	v-on:mouseout="mouseOut"
	style="cursor: pointer; margin-right: 5px">
	<img v-if="person != 'Unknown'" :src="source" alt="avatar">
	<v-icon v-else color="grey lighten-1" x-large>add</v-icon>
	</v-avatar>
</template>

<script>
//top, right, bottom, left
import { EventBus } from '@/event_bus.js'

export default {
	name: 'Person',
	props: ['person'],
	data() {
		return {}
	},

	computed: {
		source() {
			return 'http://127.0.0.1:5000/api/person_image/' + this.person
		}
	},

	methods: {
		mouseOver() {
			EventBus.$emit('face-hover', this.person)
		},
		mouseOut() {
			EventBus.$emit('face-out', this.person)
		}
	}
}
</script>

<style scoped>
</style>
