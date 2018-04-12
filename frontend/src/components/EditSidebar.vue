<template>
	<div style="padding:10px; background-color: rgba(0, 0, 0, 0.8);">
		<div>
			<v-btn block dark large @click="rotate_right">
				<v-icon x-large>rotate_right</v-icon>
			</v-btn>
			<v-btn dark class="split-button">
				<v-icon large>rotate_left</v-icon>
			</v-btn>
			<v-btn dark class="split-button" style="float:right">
				<v-icon large>flip</v-icon>
			</v-btn>
		</div>
	</div>
</template>

<script>
import axios from 'axios'
import { EventBus } from '@/event_bus.js'

export default {
	name: 'edit-sidebar',
	props: ['data'],
	components: {
	},
	data() {
		return {
			
		}
	},
	methods: {
		rotate_right() {
			axios.post(
				'http://127.0.0.1:5000/api/update_image/' +
					this.data.id,
				{ rotate: 'right' }
			)
			EventBus.$emit('image-edit', 'rotate-right')
		}
		
	},

	computed: {
	}
}


</script>

<style scoped>
.btn--large {
    height: 64px;
}

.split-button {
	margin: 0;
	width: 49%;
	height: 52px;
}



</style>
