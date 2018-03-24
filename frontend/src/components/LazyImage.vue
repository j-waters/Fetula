<template>
    <div class="wrapper">
		<!--transition-group name="fade" mode="in-out">
			<img v-show="!main" :class="['placeholder']" ref="placeholder" v-on:load="onPlaceholder" key="1"/>
			<img v-show="main" :class="['main', main ? 'loaded' : '']" ref="main" v-on:load="onMain" key="2"/>
		</transition-group-->
		<img :src="src"/>
    </div>
</template>

<script>
//:src="placeholder"

export default {
	name: 'lazy-image',
	props: ['src', 'placeholder', 'priority'],
	data() {
		return {
			main: false,
			place: false,
			placeThreshhold: 1,
			mainThreshhold: 1
		}
	},
	methods: {
		onPlaceholder() {
			this.$refs.main.src = this.src
			this.place = true
		},

		onMain() {
			this.main = true
			//window.removeEventListener('scroll', this.update)
			//clearInterval(this.interval)
		},
		/*getRect () {
			this.rect = this.$el.getBoundingClientRect()
			
		},
		checkInView (threshhold) {
			this.getRect()
			return (this.rect.top < window.innerHeight * threshhold)
		},
		update () {
			if (this.$el != undefined){
				if (this.$refs.placeholder != undefined){
					if (this.checkInView(this.placeThreshhold)) {
						this.$refs.placeholder.src = this.placeholder
					}
					else {
						this.$refs.placeholder.src = ''
					}
				}
				if (this.$refs.main != undefined){
					if (this.place){
						if (this.checkInView(this.mainThreshhold)) {
							this.$refs.main.src = this.src
						}
						else {
							this.$refs.main.src = ''
						}
					}
				}
			}
		}*/
	},

	mounted () {
		//window.addEventListener('scroll', this.update.bind(this))
		//this.interval = setInterval(this.update.bind(this), 1000)
		//setTimeout(function(){this.placeThreshhold = 1.5; this.mainThreshhold = 1.3}.bind(this), 4000)
		//setTimeout(function(){this.placeThreshhold = 5; this.mainThreshhold = 3}.bind(this), 6000)
		/*if (this.priority < 9){
			this.$refs.placeholder.src = this.placeholder
		}
		else {
			setTimeout(function() {
				this.$refs.placeholder.src = this.placeholder
			}.bind(this), 10000 + this.priority * 200)
		}*/
		//this.update()
	},
	destroyed () {
		//window.removeEventListener('scroll', this.update.bind(this))
		//clearInterval(this.interval)
	}
	
}
</script>

<style scoped>

.fade-enter-active,
.fade-leave-active {
	transition-property: opacity;
	transition-duration: 0.5s;
}

.fade-enter,
.fade-leave-active {
	opacity: 0;
}

.wrapper {
	min-height: inherit;
}

.main {
	position: absolute;
	top: 0;
	left: 0;
}

span {
    min-height: inherit;
}

.loaded {
	position: relative
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
