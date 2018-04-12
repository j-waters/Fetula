<template>
	<v-flex xs12 v-if="!hide">
		<v-card hover v-on:click.native="activate" :class="[selected ? 'card-selected' : '']">
			<v-card-title>
				<h3>Rotation</h3>
				<v-chip disabled>Confidence: {{100 - Math.round(suggestion.distance / 45 * 100)}}%</v-chip>
				<v-btn round outline color="success" @click="accept">Accept
					<v-icon right>check_circle</v-icon>
				</v-btn>
				<v-btn round outline color="error" @click="reject">Reject
					<v-icon right>block</v-icon>
				</v-btn>
			</v-card-title>
			<v-card-text>
				<thumbnail :photoid="suggestion.photo" :size="tSize" :controls="['rotate']"/>
				<thumbnail :photoid="suggestion.photo" :size="tSize" :rotate="suggestion.rotation / 90"/>
			</v-card-text>
		</v-card>
	</v-flex>
</template>

<script>
import Thumbnail from '@/components/Thumbnail.vue'
import { EventBus } from '@/event_bus.js'
import axios from 'axios'


export default {
	name: 'rotation',
	props: ['suggestion'],
	components: {
		Thumbnail,
	},

	data() {
		return {
			selected: false,
			hide: false
		}
	},

	methods: {
		activate () {
			this.selected = !this.selected
		},
		accept() {
			axios.post(
				'http://127.0.0.1:5000/api/update_image/' +
					this.suggestion.photo,
				{ rotate: 'auto' }
			)
			this.hide = true
		},
		reject() {
			axios.post(
				'http://127.0.0.1:5000/api/update_image/' +
					this.suggestion.photo,
				{ rotate: 'delete' }
			)
			this.hide = true
		}
	},

	computed: {
		tSize() {
			if (this.selected){
				return 450
			}
			return 128
		}
	},
	created() {
		EventBus.$on('image-edit', function(type){
			if (type == 'delete'){
				var total = this.suggestion.similar.length + 1
				total -= 1
				if (total < 2){
					this.hide = true
				}
			}
			
		}.bind(this))
	}
}


</script>

<style scoped>

</style>
