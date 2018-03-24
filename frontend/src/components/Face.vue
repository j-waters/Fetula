<template>
    <div class="face">
		<svg>
			<rect rx="10" ry="10" :x="rect[0] + '%'" :y="rect[1] + '%'" :width="rect[2] + '%'" :height="rect[3] + '%'" style="fill: transparent;stroke-width: 3;stroke: greenyellow;" />
		</svg>

		<svg v-if="hovered">
			<rect rx="10" ry="10" :x="rect[0] + '%'" :y="rect[1] + '%'" :width="rect[2] + '%'" :height="rect[3] + '%'" style="fill: transparent;stroke-width: 3;stroke: red;" />
		</svg>
    </div>
</template>

<script>
import { EventBus } from '@/event_bus.js'

export default {
	name: 'Face',
	props: ['face'],
	data() {
		return {
			hovered: false
		}
	},

	computed: {
		rect(){
			return this.face.position
		}
	},

	created() {
		EventBus.$on('face-hover', function(face){
			if (face == this.face.name){
				this.hovered = true
			}
			else {
				this.hovered = false
			}
			
		}.bind(this))

		EventBus.$on('face-out', function(face){
			
			if (face == this.face.name){
				this.hovered = false
			}
			
		}.bind(this))
	}
	
}
</script>

<style scoped>
.face {
	position: absolute;
	top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

svg {
	position: absolute;
	top: 0;
    left: 0;
	width: 100%;
    height: 100%;
}
</style>
