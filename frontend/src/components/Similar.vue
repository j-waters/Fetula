<template>
	<v-flex xs12 v-if="!hide">
		<v-card hover v-on:click.native="activate" :class="[selected ? 'card-selected' : '']">
			<v-card-title>
				<h3>Similar</h3>
				<v-chip disabled>{{suggestion.similar.length + 1}}</v-chip>
				<v-btn v-if="suggestion.similar.length > 6" round outline color="success"
					   v-on:click.native.stop="animate">Create Animation
					<v-icon right>movie</v-icon>
				</v-btn>
			</v-card-title>
			<v-card-text>
				<thumbnail :key="suggestion.parent" :photoid="suggestion.parent" :size="tSize" :controls="['delete']"/>
				<v-tooltip v-for="photo in suggestion.similar" bottom :key="photo[0]">
					<thumbnail slot="activator" :photoid="photo[0]" :size="tSize" :controls="['delete']"/>
					<span>Confidence: {{Math.round(100 - (photo[1]/64 * 100))}}%</span>
				</v-tooltip>
			</v-card-text>
		</v-card>
	</v-flex>
</template>

<script>
import Thumbnail from '@/components/Thumbnail.vue'
import { EventBus } from '@/event_bus.js'
import axios from 'axios'

export default {
	name: 'similar',
	props: ['suggestion'],
	components: {
		Thumbnail
	},

	data() {
		return {
			selected: false,
			hide: false
		}
	},

	methods: {
		activate() {
			this.selected = !this.selected
		},

		animate() {
			var photos = [this.suggestion.parent]
			for (var i in this.suggestion.similar) {
				photos.push(this.suggestion.similar[i][0])
			}
			axios
				.post('http://127.0.0.1:5000/api/create_animation', {
					photos: photos
				})
				.then(response => {

				})
		}
	},

	computed: {
		tSize() {
			if (this.selected) {
				return 450
			}
			return 128
		}
	},
	created() {
		EventBus.$on(
			'image-edit',
			function(type) {
				if (type == 'delete') {
					var total = this.suggestion.similar.length + 1
					total -= 1
					if (total < 2) {
						this.hide = true
					}
				}
			}.bind(this)
		)
	}
}


</script>

<style scoped>
</style>
