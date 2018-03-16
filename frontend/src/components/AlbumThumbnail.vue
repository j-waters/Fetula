<template>
  <v-card hover class="photo" height="128px">
    <!--img :src="source" @click="activate"-->
    <div class="progressive" @click="activate" v-on:mouseover="hover = true" v-on:mouseleave="hover = false">
      <img class="preview" v-progressive="source + '/s'" :src="source + '/xs'"/>
    <div class="caption">
                            <div><p>{{name}}</p>
                            </div>
                        </div>
		<v-icon style="position: absolute; z-index: 999; color: white; right: 0;">photo_album</v-icon>
    </div>
  </v-card>
</template>

<script>
import axios from 'axios'

export default {
	name: 'album-thumbnail',
	props: ['albumid'],
	data() {
		return {
			hover: false,
			fetching: false,
			name: '',
			albums: []
		}
	},
	methods: {
		activate () {
			console.log('click')
			//this.$router.push({ name: 'album', query: { album: this.albumid } })
		},
		mouseOver () {
			this.hover = !this.hover
		},
		fetchMeta() {
			if (this.fetching != true) {
				this.fetching = true
				axios
					.get('http://127.0.0.1:5000/api/album_data/' + this.albumid)
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
  margin-right: 5px;
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
