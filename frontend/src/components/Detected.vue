<template>
	<div class="detected">
		<svg>
			<rect rx="10" ry="10" :x="rect[0] + '%'" :y="rect[1] + '%'" :width="rect[2] + '%'" :height="rect[3] + '%'"
				  :style="{'fill': 'transparent', 'stroke-width': 3, 'stroke': colour}"/>
		</svg>

		<svg v-if="hovered">
			<rect rx="10" ry="10" :x="rect[0] + '%'" :y="rect[1] + '%'" :width="rect[2] + '%'" :height="rect[3] + '%'"
				  style="fill: transparent;stroke-width: 3;stroke: red;"/>
		</svg>
	</div>
</template>

<script>
import { EventBus } from '@/event_bus.js'

export default {
	name: 'Detected',
	props: ['detected', 'colour'],
	data() {
		return {
			hovered: false
		}
	},

	computed: {
		rect(){
			return this.detected.position
		}
	},

	created() {
		EventBus.$on('detected-hover', function(detected){
			if (detected == this.detected.name){
				this.hovered = true
			}
			else {
				this.hovered = false
			}
			
		}.bind(this))

		EventBus.$on('detected-out', function(detected){
			
			if (detected == this.detected.name){
				this.hovered = false
			}
			
		}.bind(this))
	}
	
}


</script>

<style scoped>
.detected {
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
