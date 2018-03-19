<template>
	<div :class="['thumb-pad', 'aspect-' + ratio]">
		<v-card hover class="photo" :height="size + 'px'" v-on:mouseover="hover = true" v-on:mouseleave="hover = false" v-on:click.native.stop="activate">
			<progressive-img
				:src="source + modifier"
				@onLoad="get_ratio"
				/>
				<transition name="hover">
					
			<div class="caption" v-show="true">
									<div><p>{{name}}</p>
									</div>
									</div>
								
			</transition>
			<v-icon style="position: absolute; z-index: 999; color: white; right: 0; top:0;">photo_album</v-icon>
		</v-card> 
  </div>
</template>

<script>
//:placeholder="source + '/xs'"	
import axios from 'axios'

export default {
	name: 'album-thumbnail',
	props: ['albumid', 'size'],
	data() {
		return {
			hover: false,
			fetching: false,
			name: '',
			albums: [],
			ratio: '4x3'
		}
	},
	methods: {
		activate () {
			this.$router.push({ name: 'album', query: { album: this.albumid } })
		},
		mouseOver () {
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
					.get('http://127.0.0.1:5000/api/album_data/' + this.albumid + '/s')
					.then(response => {
						this.fetching = false
						this.name = response.data.name
					})
					.catch(e => {
						console.log(e.message)
					})
			}
		}
	},

	computed: {
		source() {
			return 'http://127.0.0.1:5000/api/image/' + this.albumid + '/A'
		},
		
		modifier() {
			if (parseInt(this.size) > 150){
				return '/m'
			}
			else {
				return '/s'
			}
		}
	},

	created() {
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

img {
  height: 128px;
}

.progressive img {
  width: auto;
  height: 129px;
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
	padding: 2em 2em 0.75em 1em;
	position: absolute;
	bottom: 0;
	left: 0;
	width: 100%;
	color: rgba(255, 255, 255, 0.9);
	z-index: 1;
	font-size: 14px !important
}

p {
    margin-bottom: 0;
}
</style>