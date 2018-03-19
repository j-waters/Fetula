<template>
    <v-layout>
      <v-flex :class="{'flex xs9': !isFull, 'flex xs12': isFull, 'picture': true}" style="background-color: #000000;">
          <div class="imgpanel" style="position: relative; height: 100vh;">
            
                <div class="imgwrap">
                    <!--img :src="source + '/s'"-->
                    <clazy-load :src="source + '/l'">
                        <img :src="source + '/l'" slot="image">
                        <div class="caption" slot="image">
                            <h2>{{data.album.name}}</h2> 
                            <div><p>{{fdate}}</p>
                            </div>
                        </div>
                    </clazy-load>
					<transition-group name="face">
						<face v-if="!isFull" v-for="face in data.faces" :key="face[1]" :face="face"/>
					</transition-group>
                    
                </div>
				<img v-if="data.album.size > parseInt(this.$route.query.photo) + 1" src="@/assets/arrow.svg" class="nav-next" v-on:click="selectNext()">
            	<img v-if="parseInt(this.$route.query.photo) - 1 >= 0" src="@/assets/arrow.svg" class="nav-previous" v-on:click="selectPrev()">
            
            <div class="menus">
				<v-btn icon @click="star">
					<v-icon>{{(data.star) ? 'star' : 'star_outline'}}</v-icon>
				</v-btn>
				<v-btn icon @click="isFull = !isFull">
					<v-icon>info</v-icon>
				</v-btn>
            </div>
			<div class="backbutton">
				<v-btn icon @click="$router.go(-1)">
					<v-icon class="button">arrow_back</v-icon>
				</v-btn>
			</div>
          </div>
      </v-flex>
        <transition name="expand">
            <v-flex class="flex xs3 menu" v-if="!isFull">
                <view-details :data='data' :show="!isFull"></view-details>
				
            </v-flex>
        </transition>
    </v-layout>
</template>

<script>
import axios from 'axios'
import ViewDetails from '@/components/ViewDetails.vue'
import Face from '@/components/Face.vue'
//router.replace won't add new history
export default {
	name: 'viewer',
	//props: ['album', 'photo'],
	components: { ViewDetails, Face },
	data() {
		return {
			isFull: true,
			data: {
				tags: ['dog', 'cat', 'person', 'city'],
				album: { name: '', range:[0, 0] }
			}
		}
	},
	watch: {
		// call again the method if the route changes
		'$route': 'fetchData'
	},
	computed: {
		source() {
			return (
				'http://127.0.0.1:5000/api/image/' +
				this.$route.query.album +
				'/' +
				this.$route.query.photo
			)
		},

		fdate() {
			var date = new Date(this.data.date)
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
		}
	},

	methods: {
		selectNext() {
			this.$router.replace({
				name: 'view',
				query: {
					album: this.$route.query.album,
					photo: parseInt(this.$route.query.photo) + 1
				}
			})
		},
		selectPrev() {
			this.$router.replace({
				name: 'view',
				query: {
					album: this.$route.query.album,
					photo: parseInt(this.$route.query.photo) - 1
				}
			})
		},
		preload() {
			const pre = new Image()
			pre.src =
				'http://127.0.0.1:5000/api/image/' +
				this.$route.query.album +
				'/' +
				this.$route.query.photo +
				'/l'

			const pre1 = new Image()
			pre1.src =
				'http://127.0.0.1:5000/api/image/' +
				this.$route.query.album +
				'/' +
				(parseInt(this.$route.query.photo) + 1) +
				'/l'

			const pre2 = new Image()
			pre2.src =
				'http://127.0.0.1:5000/api/image/' +
				this.$route.query.album +
				'/' +
				(parseInt(this.$route.query.photo) - 1) +
				'/l'
		},

		fetchData() {
			axios
				.get(
					'http://127.0.0.1:5000/api/metadata/' +
						this.$route.query.album +
						'/' +
						this.$route.query.photo +
						'/n'
				)
				.then(response => {
					this.data = response.data
				})
				.catch(e => {
					console.log(e.message)
				})
			this.preload()
		},

		star() {
			this.data.star = !this.data.star
			axios.post(
				'http://127.0.0.1:5000/api/update/' +
					this.$route.query.album +
					'/' +
					this.$route.query.photo,
				{ star: this.data.star }
			)
		}
	},

	mounted() {
		this.preload()
	},

	created() {
		this.fetchData()
	}
}
</script>

<style scoped>
.nav-next,
.nav-previous {
	-webkit-tap-highlight-color: transparent;
	position: absolute;
	top: 50%;
	width: 6em;
	height: 6em;
	margin-top: -3em;
	cursor: pointer;
}

.nav-previous {
	-moz-transform: scaleX(-1);
	-webkit-transform: scaleX(-1);
	-ms-transform: scaleX(-1);
	transform: scaleX(-1);
	left: 0;
}

.nav-next {
	right: 0;
}

.menu {
	background-color: #fff;
}

.row {
	background-color: #000000;
}

.btn {
	color: rgba(255, 255, 255, 0.85)
}

.expand-enter-active,
.expand-leave-active {
	transition-property: transform, max-width, opacity;
	transition-duration: 0.8s, 0.8s, 0.6s;
}

.expand-enter-active {
	transition-delay: 0s, 0s, 0.2s;
}

.expand-enter,
.expand-leave-active {
	flex-basis: 0;
	max-width: 0;
	opacity: 0;
}


.face-enter-active,
.face-leave-active {
	transition-property: opacity;
	transition-duration: 0.8s;
}

.face-enter-active {
	transition-delay: 0.1s;
}

.face-enter,
.face-leave-active {
	opacity: 0;
}

.picture {
	transition: all 0.8s;
}

body {
	overflow: hidden;
}

.menus {
	position: absolute;
	top: 0;
	right: 0;
	z-index: 20;
	padding: 5px;
}

.backbutton {
	color: rgba(255, 255, 255, 0.85);
	position: absolute;
	top: 0;
	left: 0;
	z-index: 20;
	padding: 5px;
	cursor: pointer;
}

img {
	max-width: 100%;
	/*left: 50%;
	transform: translate(-50%, 0);*/
	animation-name: zoom;
	animation-duration: 0.8s;
	max-height: 100vh;
	display: block;
}

.imgwrap {
	position: relative;
	left: 50%;
	top: 50%;
	transform: translate(-50%, -50%);
	max-width: fit-content;
	max-height: 100vh;
}

@keyframes zoom {
	from {
		/*max-width: 0;*/
		max-height: 0;
	}
	to {
		/*max-width: auto;*/
		max-height: 99vh;
	}
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
	color: rgba(255, 255, 255, 0.5);
	z-index: 1;
}

.caption h2,
.caption h3 {
	color: #fff;
}

.caption div {
	margin: 0;
	padding: 0;
	border: 0;
	font-size: 100%;
	font: inherit;
	vertical-align: baseline;
}
</style>
