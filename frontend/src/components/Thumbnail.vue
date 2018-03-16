<template>
  <v-card hover class="photo" :height="size + 'px'">
    <!--img :src="source" @click="activate"-->
    <div class="progressive" @click="activate" v-on:mouseover="hover = true" v-on:mouseleave="hover = false">
      <img class="preview" v-progressive="source + '/s'" :src="source + '/xs'"/>
      <transition name="hover">
    <div class="caption" v-show="hover">
                            <div><p>{{fdate}}</p>
                            </div>
														<div><p>{{ftime}}</p>
                            </div>
                        </div>
      </transition>
    </div>
  </v-card>
</template>

<script>
import axios from 'axios'

export default {
	name: 'Thumbnail',
	props: ['album', 'photoid', 'size'],
	data() {
		return {
			hover: false,
			date: new Date()
		}
	},
	methods: {
		activate() {
			this.$router.push({
				name: 'view',
				query: { album: this.album, photo: this.photoid }
			})
		},
		mouseOver() {
			this.hover = !this.hover
		},
		fetchMeta() {
			if (this.fetching != true) {
				this.fetching = true
				axios
					.get('http://127.0.0.1:5000/api/metadata/' + this.album + '/' + this.photoid + '/s')
					.then(response => {
						this.fetching = false
						this.date = new Date(response.data.date)
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

		fdate() {
			var date = this.date
			var monthNames = [
				"January", "February", "March",
				"April", "May", "June", "July",
				"August", "September", "October",
				"November", "December"
			];

			var day = date.getDate();
			var monthIndex = date.getMonth();
			var year = date.getFullYear();

			return day + ' ' + monthNames[monthIndex] + ' ' + year;
		},

		ftime() {
			var date = this.date

			var hour = date.getHours()
			var minute = date.getMinutes().toString()

			return hour + ":" + minute.padStart(2, '0')
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

.progressive {
	height: inherit
}

.progressive img {
	height: inherit;
	width: auto;
}

.photo {
  margin-right: 5px;
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
