<template>
	<div :class="['wrapper', 'aspect-' + calc_ratio]">
		<transition-group name="fade" mode="in-out">
			<img :class="['blank']" ref="blank" :src="blank" key="0" v-on:load="update"/>
			<img v-show="!main && place" :class="['placeholder']" ref="placeholder" v-on:load="onPlaceholder" key="1"/>
			<img v-show="main" :class="['main', main ? 'loaded' : '']" ref="main" v-on:load="onMain" key="2"
				 :style="rotate"/>
		</transition-group>
    </div>
</template>

<script>
//:src="placeholder"

export default {
	name: 'lazy-image',
	//props: ['src', 'placeholder', 'ratio', 'rotation'],
	props: {
		src: String,
		placeholder: String,
		ratio: String,
		rotation : {
			type: Number,
			default: 0
		}
	},
	data() {
		return {
			main: false,
			place: false,
			placeThreshhold: 2,
			mainThreshhold: 1.2
		}
	},

	watch: {
		'src': function(){
			this.$refs.main.src = this.src
		},

		'rotation': function(){
			/*if (this.rect == undefined){
				this.$el.getBoundingClientRect()
			}
			this.$refs.main.style['min-height'] = this.rect.width + 'px'
			this.$refs.main.style['min-width'] = this.rect.height + 'px'*/
		}
	},
	computed: {
		blank() {
			if (this.calc_ratio == '4x3') {
				return 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAADCAYAAAC09K7GAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAZdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuMjHxIGmVAAAAEklEQVQYV2P4//8/CiYk8J8BAKS4I91wF3n4AAAAAElFTkSuQmCC'
			}
			if (this.calc_ratio == '3x4') {
				return 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAMAAAAECAYAAABLLYUHAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAZdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuMjHxIGmVAAAAEklEQVQYV2P4//8/HBPF+c8AALanI92Pb/HEAAAAAElFTkSuQmCC'
			}
			if (this.calc_ratio == '614x135') {
				return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmYAAACHCAMAAACLdWW2AAAABGdBTUEAALGPC/xhBQAAAwBQTFRFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAszD0iAAAAQB0Uk5T////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////AFP3ByUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAAZdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuMjHxIGmVAAABWklEQVR4Xu3SMQEAMBADofo3nar4m0ADb3BOMwKaEdCMgGYENCOgGQHNCGhGQDMCmhHQjIBmBDQjoBkBzQhoRkAzApoR0IyAZgQ0I6AZAc0IaEZAMwKaEdCMgGYENCOgGQHNCGhGQDMCmhHQjIBmBDQjoBkBzQhoRkAzApoR0IyAZgQ0I6AZAc0IaEZAMwKaEdCMgGYENCOgGQHNCGhGQDMCmhHQjIBmBDQjoBkBzQhoRkAzApoR0IyAZgQ0I6AZAc0IaEZAMwKaEdCMgGYENCOgGQHNCGhGQDMCmhHQjIBmBDQjoBkBzQhoRkAzApoR0IyAZgQ0I6AZAc0IaEZAMwKaEdCMgGYENCOgGQHNCGhGQDMCmhHQjIBmBDQjoBkBzQhoRkAzApoR0IyAZgQ0I6AZAc0IaEZAMwKaEdCMgGYENCOgGQHNCGhGQDMCmhHQjIBmBDQjoBnntg/SzpkVJZ216QAAAABJRU5ErkJggg=="
			}
		},
		
		calc_ratio(){
			if (this.ratio == '4x3'){
				if (this.rotation % 2 != 0){
					return '3x4'
				}
				return '4x3'
			}
			if (this.ratio == '3x4'){
				if (this.rotation % 2 != 0){
					return '4x3'
				}
				return '3x4'
			}
			return this.ratio
		},
		rotate(){
			var out = {'transform': 'rotate(' + 90 * this.rotation + 'deg)'}
			if (this.rotation % 4 == 0){
			}
			else if (this.rotation % 3 == 0){
				if (this.ratio == '4x3'){
					out['margin-top'] = '133.3%'
					out['transform-origin'] = '0 0'
					out['max-width'] = '133.3%'
					out['min-height'] = '75%'
				}
				if (this.ratio == '3x4'){
					out['transform-origin'] = '0 0'
					out['margin-top'] = '75%'
					out['min-width'] = '75%'
				}

			}
			else if (this.rotation % 2 == 0){

			}
			else if (this.rotation % 1 == 0){
				if (this.ratio == '4x3'){
					out['margin-left'] = '100%'
					out['transform-origin'] = '0 0'
					out['max-width'] = '133.3%'
					out['min-height'] = '75%'
				}
				if (this.ratio == '3x4'){
					out['transform-origin'] = '0 0'
					out['margin-left'] = '100%'
					out['min-width'] = '75%'
				}
			}
			return out
		},
	},
	methods: {
		onPlaceholder() {
			//this.$refs.main.src = this.src
			this.place = true
			if (this.$refs.main){
				this.update()
			}
		},

		onMain() {
			this.main = true
		},
		update() {
			this.rect = this.$el.getBoundingClientRect()
			if (this.place){
				var inView = this.rect.top < window.innerHeight * this.mainThreshhold
				if (inView){
					this.$refs.main.src = this.src
					this.removeListeners()
				}
				else {
					//console.log("don't load main")
				}
			}
			else {
				var inView = this.rect.top < window.innerHeight * this.placeThreshhold
				if (inView){
					this.$refs.placeholder.src = this.placeholder
					//console.log("load placeholder")
				}
				else {
					//console.log("don't load placeholder")
				}
			}
		},
		removeListeners() {
			window.removeEventListener('scroll', this.boundUpdate)
			clearTimeout(this.timeout1)
			clearTimeout(this.timeout2)
		}
	},

	mounted() {
		this.boundUpdate = this.update.bind(this)
		window.addEventListener('scroll', this.boundUpdate)
		this.timeout1 = setTimeout(function(){
			this.placeThreshhold = 4
			this.mainThreshhold = 3
			this.update()
		}.bind(this), 5000)
		this.timeout2 = setTimeout(function(){
			this.placeThreshhold = 6
			this.mainThreshhold = 5
			this.update()
		}.bind(this), 15000)
	},
	destroyed() {
		this.removeListeners()
	},
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
	transition-property: opacity;
	transition-duration: 2s;
}

.fade-leave-active {
	transition-delay: 1s;
}

.fade-enter,
.fade-leave-active {
	opacity: 0;
}

.wrapper {
	min-height: inherit;
}

.main, .placeholder {
	position: absolute;
	top: 0;
	left: 0;
}

.placeholder {
    max-height: 100%;
}

span {
	min-height: inherit;
}

.unloaded {
	display: none;
}

img {
	display: block;
	min-height: inherit;
	min-width: 100%;
	max-width: 100%;
}
</style>
