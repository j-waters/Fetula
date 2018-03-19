<template >
	<div :class="['thumb-pad', 'aspect-' + ratio]">
		<v-card hover class="photo" :height="size + 'px'" v-on:mouseover="hover = true" v-on:mouseleave="hover = false" v-on:click.native.stop="activate">
		<progressive-img
			:src="source + modifier"
			
			@onLoad="get_ratio"
			/>
			<transition name="hover">
				
		<div class="caption" v-show="hover">
								<div><p>{{fdate}}</p>
								</div>
															<div><p>{{ftime}}</p>
								</div>
							</div>
		</transition>
	</v-card> 
	</div>
</template>

<script>
//:placeholder="source + '/xs'"
import axios from 'axios'
import imagesLoaded from 'vue-images-loaded'

export default {
	name: 'Thumbnail',
	props: ['album', 'photoid', 'size'],
	data() {
		return {
			hover: false,
			date: new Date(),
			fetched: false,
			ratio: '4x3'
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
		get_ratio() {
			var c = this.$children[0].$children[0].$el.children
			let img = c[c.length - 1].children[0]
			img.onload = function(i){
				img = i.target
				var w = img.naturalWidth
				var h = img.naturalHeight
				var r = w / h
				if (Math.round(r * 3, 2) == 4) {
					this.ratio = '4x3'
				}
				if (Math.round(r * 4, 2) == 3) {
					this.ratio = '3x4'
				}
			}.bind(this)
			
		},
		fetchMeta() {
			if (this.fetching != true) {
				this.fetching = true
				axios
					.get(
						'http://127.0.0.1:5000/api/metadata/' +
							this.album +
							'/' +
							this.photoid +
							'/s'
					)
					.then(response => {
						this.fetching = false
						this.date = new Date(response.data.date)
						//this.ratio = response.data.ratio
					})
					.catch(e => {
						console.log(e.message)
					})
			}
		}
	},

	computed: {
		source() {
			return (
				'http://127.0.0.1:5000/api/image/' +
				this.album +
				'/' +
				this.photoid
			)
		},

		modifier() {
			if (parseInt(this.size) > 150) {
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

.hover-enter-active,
.hover-leave-active {
	transition-property: opacity;
	transition-duration: 0.5s;
}

.hover-enter,
.hover-leave-active {
	opacity: 0;
}

.photo {
  margin-bottom: 5px;
  display: inline-block;
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
</style>

<style>
.progressive-image-main {
	height: inherit;
	width: auto;
	position: relative;
}
.progressive-image-wrapper {
	padding-bottom: 0 !important;
	height: inherit;
}

.progressive-image {
	height: inherit;
}
</style>
