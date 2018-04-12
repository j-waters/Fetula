<template >
	<div :class="[flex ? 'thumb-flex' : 'thumb-block', 'aspect-' + ratio]" v-if="!hide">
		<v-card hover class="photo" :style="{'min-height': size + 'px'}" v-on:mouseover="hover = true" v-on:mouseleave="hover = false" v-on:click.native.stop="activate">
		<!--progressive-img
			:src="source + modifier"
			@onLoad="get_ratio"
			/-->
			<lazy-image :placeholder="source + '/xs' + p_version" :src="source + modifier + p_version"
						:ratio="base_ratio" :rotation="rotate"/>
			<div class="controls">
				<v-btn icon v-if="controls.indexOf('rotate') != -1 && hover" v-on:click.native.stop="rotate_right">
					<v-icon color="white" small>rotate_right</v-icon>
				</v-btn>
				<v-btn icon v-if="controls.indexOf('delete') != -1 && hover" v-on:click.native.stop="del">
					<v-icon color="white" small>delete</v-icon>
				</v-btn>
			</div>
			<transition name="hover">
				<div class="caption" v-show="hover">
					<div><p>{{fdate}}</p></div>
					<div><p>{{ftime}}</p></div>
				</div>
			</transition>
		</v-card>
	</div>
</template>

<script>
//:placeholder="source + '/xs'"			//this does not work
import axios from 'axios'
import imagesLoaded from 'vue-images-loaded'
import LazyImage from '@/components/LazyImage.vue'
import { EventBus } from '@/event_bus.js'

export default {
	name: 'Thumbnail',
	//props: ['photoid', 'size', 'flex', 'controls'],
	props: {
		photoid: Number,
		size: Number,
		flex: Boolean,
		controls: {
			type: Array,
			default: function() {
				return []
			}
		},
		rotate: {
			type: Number,
			default: 0
		}
	},
	components: { LazyImage },
	data() {
		return {
			hover: false,
			date: new Date(),
			fetched: false,
			base_ratio: '4x3',
			hide: false,
			version: 0
		}
	},
	directives: {
		imagesLoaded
	},
	methods: {
		activate() {
			this.$router.push({
				name: 'view',
				query: { album: this.album, photo: this.photoid }
			})
		},
		loaded() {
			this.fetched = true
		},
		mouseOver() {
			this.hover = !this.hover
		},
		fetchMeta() {
			if (this.fetching != true) {
				this.fetching = true
				axios
					.get(
						'http://127.0.0.1:5000/api/metadata/' +
							this.photoid +
							'/s'
					)
					.then(response => {
						this.fetching = false
						this.date = new Date(response.data.date)
						this.base_ratio = response.data.ratio
						this.version = response.data.version
					})
					.catch(e => {
						console.log(e.message)
					})
			}
		},

		del() {
			axios.post(
				'http://127.0.0.1:5000/api/update_image/' + this.photoid,
				{ delete: true }
			)
			this.hide = true
		},
		rotate_right() {
			axios.post(
				'http://127.0.0.1:5000/api/update_image/' +
					this.photoid,
				{ rotate: 'right' }
			)
			this.rotate += 1
			//this.version += 1
		}
	},

	computed: {
		source() {
			return 'http://127.0.0.1:5000/api/image/' + this.photoid
		},

		ratio(){
			if (this.base_ratio == '4x3'){
				if (this.rotate % 2 != 0){
					return '3x4'
				}
				return '4x3'
			}
			if (this.base_ratio == '3x4'){
				if (this.rotate % 2 != 0){
					return '4x3'
				}
				return '3x4'
			}
			return this.base_ratio
		},

		p_version() {
			return '?v=' + this.version
		},

		modifier() {
			if (parseInt(this.size) > 400) {
				return '/ml'
			} else if (parseInt(this.size) > 150) {
				return '/m'
			} else {
				return '/s'
			}
		},

		fdate() {
			var date = this.date
			var monthNames = [
				'January',
				'February',
				'March',
				'April',
				'May',
				'June',
				'July',
				'August',
				'September',
				'October',
				'November',
				'December'
			]

			var day = date.getDate()
			var monthIndex = date.getMonth()
			var year = date.getFullYear()

			return day + ' ' + monthNames[monthIndex] + ' ' + year
		},

		ftime() {
			var date = this.date

			var hour = date.getHours()
			var minute = date.getMinutes().toString()

			return hour + ':' + minute.padStart(2, '0')
		}
	},

	mounted() {
		this.fetchMeta()
	}
}
</script>

<style scoped lang="css">

.card {
	transition: min-height 1s;
}

.thumb-flex {
	flex: auto;
	margin: 2px;
	
}

.thumb-block {
	display: inline-block;
	margin-right: 5px;
}

.hover-enter-active,
.hover-leave-active {
	transition-property: opacity;
	transition-duration: 0.2s;
}

.hover-enter,
.hover-leave-active {
	opacity: 0;
}

.photo {
  margin-bottom: 5px;
  display: inline-block;
  min-width: 100%;
}

.caption {
	background-image: -moz-linear-gradient(
		bottom,
		rgba(16, 16, 16, 0.75),
		rgba(16, 16, 16, 0.25) 80%,
		rgba(16, 16, 16, 0)
	);
	background-image: -webkit-linear-gradient(
		bottom,
		rgba(16, 16, 16, 0.75),
		rgba(16, 16, 16, 0.25) 80%,
		rgba(16, 16, 16, 0)
	);
	background-image: -ms-linear-gradient(
		bottom,
		rgba(16, 16, 16, 0.75),
		rgba(16, 16, 16, 0.25) 80%,
		rgba(16, 16, 16, 0)
	);
	background-image: linear-gradient(
		bottom,
		rgba(16, 16, 16, 0.75),
		rgba(16, 16, 16, 0.25) 80%,
		rgba(16, 16, 16, 0)
	);
	padding: 2em 2em 0.75em 2em;
	position: absolute;
	bottom: 0;
	left: 0;
	width: 100%;
	color: rgba(255, 255, 255, 0.8);
	z-index: 1;
}

p {
    margin-bottom: 0;
}

.controls {
	top: 0;
    position: absolute;
    right: 0;
}

.btn {
    margin: 6px 0 6px 0;
}
</style>
