<template>
    <v-layout>
      <v-flex :class="{'flex xs9': !isFull, 'flex xs12': isFull, 'picture': true}" style="background-color: #000000;">
          <div class="imgpanel" style="position: relative; height: 100vh;">
            
                <div class="imgwrap">
                    <!--img :src="source + '/s'"-->
					<img ref="main" slot="image" v-on:load="loadedHQ=true" :style="rotation">
					<div v-show="fetchedMeta" class="caption" slot="image">
                            <h2>{{data.album.name}}</h2> 
                            <div><p>{{fdate}}</p>
                            </div>
                        </div>
					<transition-group name="face">
						<detected v-if="!isFull" v-for="face in data.people" :key="face.name" :detected="face"
								  :colour="'greenyellow'"/>
						<detected v-if="!isFull" v-for="tag in data.tags" :key="tag.position[0] + tag.name"
								  :detected="tag" :colour="'blue'"/>
					</transition-group>
                    
                </div>
			  <img v-if="data.album.next != null" src="@/assets/arrow.svg" class="nav-next" v-on:click="selectNext()">
			  <img v-if="data.album.prev != null" src="@/assets/arrow.svg" class="nav-previous"
				   v-on:click="selectPrev()">
            
            <div class="menus">
				<v-btn icon @click="star">
					<v-icon>{{(data.star) ? 'star' : 'star_outline'}}</v-icon>
				</v-btn>
				<v-btn icon @click="openLocal">
					<v-icon>open_in_browser</v-icon>
				</v-btn>
				<v-btn icon @click="editBar = !editBar">
					<v-icon>edit</v-icon>
				</v-btn>
				<v-btn icon @click="quality" v-if="!(loadedHQ && loadHQ)">
					<v-icon :class="{'pulse': loadHQ}">high_quality</v-icon>
				</v-btn>
				<v-btn icon @click="detailsBar = !detailsBar">
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
				<view-details :data='data' v-show="detailsBar"></view-details>
				<edit-sidebar :data='data' v-show="editBar"></edit-sidebar>
            </v-flex>
        </transition>
    </v-layout>
</template>

<script>
import axios from 'axios'
import ViewDetails from '@/components/ViewDetails.vue'
import EditSidebar from '@/components/EditSidebar.vue'
import Detected from '@/components/Detected.vue'
import { EventBus } from '@/event_bus.js'

//router.replace won't add new history
export default {
	name: 'viewer',
	//props: ['album', 'photo'],
	components: { ViewDetails, Detected, EditSidebar },
	data() {
		return {
			detailsBar: false,
			editBar: false,
			imgSize: '/l',
			loadHQ: false,
			loadedHQ: false,
			fetchedMeta: false,
			data: {
				tags: ['dog', 'cat', 'person', 'city'],
				album: { name: '', range:[0, 0] },
				people: []
			},
			rotate: 0,
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
				this.$route.query.photo
			)
		},
		p_version() {
			return '?v=' + this.data.version
		},

		rotation(){
			return {'transform': 'rotate(' + 90 * this.rotate + 'deg)'}
		},

		isFull() {
			return !(this.detailsBar || this.editBar)
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
		openLocal() {
			window.location = "ms-photos:viewer?fileName=" + this.data.path
		},
		quality() {
			this.imgSize = '/o'
			this.loadedHQ = false
			this.loadHQ = true
			this.$refs.main.src = this.source + this.imgSize + this.p_version
		},
		selectNext() {
			this.selectImage()
			this.$router.replace({
				name: 'view',
				query: {
					album: this.$route.query.album,
					photo: this.data.album.next
				}
			})
		},
		selectPrev() {
			this.selectImage()
			this.$router.replace({
				name: 'view',
				query: {
					album: this.$route.query.album,
					photo: this.data.album.prev
				}
			})
		},
		selectImage() {
			this.imgSize = '/l'
			this.loadHQ = false
			this.loadedHQ = false
		},
		preload() {
			const pre = new Image()
			pre.src =
				'http://127.0.0.1:5000/api/image/' +
				this.$route.query.photo +
				'/l' + this.p_version
			if (this.data.album.next){
				const pre1 = new Image()
				pre1.src =
					'http://127.0.0.1:5000/api/image/' +
					this.data.album.next +
					'/l'
			}
			if (this.data.album.prev){
				const pre2 = new Image()
				pre2.src =
					'http://127.0.0.1:5000/api/image/' +
					this.data.album.prev +
					'/l'
			}
		},

		fetchData() {
			axios
				.get(
					'http://127.0.0.1:5000/api/metadata/' +
						this.$route.query.photo +
						'/n'
				)
				.then(response => {
					this.data = response.data
					this.$refs.main.src = this.source + this.imgSize + this.p_version
					this.fetchedMeta = true
				})
				.catch(e => {
					console.log(e.message)
				})
			this.preload()
		},

		star() {
			this.data.star = !this.data.star
			axios.post(
				'http://127.0.0.1:5000/api/update_image/' +
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
		EventBus.$on('image-edit', function(type){
			if (type == 'rotate-right'){
				this.rotate += 1
				console.log(this.rotate)
			}
		}.bind(this))
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

.pulse {
	animation: pulse 1s infinite linear;
}

@keyframes pulse {
    0% {
        transform: scale(1)
    }

    50% {
        transform: scale(0.8)
    }
	0% {
        transform: scale(1)
    }
}
</style>
