<template>
<div>
	<v-toolbar flat>
		<v-btn icon @click="$router.go(-1)">
			<v-icon>arrow_back</v-icon>
		</v-btn>
		<v-spacer></v-spacer>
		<v-btn icon>
			<v-icon>more_vert</v-icon>
		</v-btn>
	</v-toolbar>
	<v-container v-scroll="onScroll">
	<v-layout row>
		<v-text-field
          name="input-1"
          id="title"
		  :hint="albumRange"
		  persistent-hint
		  :value="name"
		  @input="change_name"
        ></v-text-field>
	</v-layout>
	<v-layout row wrap>
    <album-thumbnail v-for="album in albums" :albumid="album" :key="'a' + album" :size="256" :flex="true"/>
		<thumbnail v-for="photo in photos" :key="photo" :photoid="photo" :size="256" :flex="true"
				   :controls="['delete', 'rotate']"/>
	</v-layout>
</v-container>
	<transition name="drop">
		<v-btn
				color="pink"
				dark
				medium
				fixed
				bottom
				right
				fab
				@click="$vuetify.goTo(0)"
				v-if="toTop"
		>
			<v-icon>keyboard_arrow_up</v-icon>
		</v-btn>
	</transition>
</div>
</template>

<script>
import Thumbnail from '@/components/Thumbnail.vue'
import AlbumThumbnail from '@/components/AlbumThumbnail.vue'
import axios from 'axios'

export default {
	name: 'home',
	components: {
		Thumbnail,
		AlbumThumbnail
	},

	data() {
		return {
			albums: [],
			photos: [],
			name: '',
			range: [0, 0],
			toTop: false
		}
	},
	watch: {
		// call again the method if the route changes
		'$route': 'fetchData'
	},
	computed: {
		albumRange() {
			var monthNames = [
				'Jan',
				'Feb',
				'Mar',
				'Apr',
				'May',
				'Jun',
				'Jul',
				'Aug',
				'Sep',
				'Oct',
				'Nov',
				'Dec'
			]

			var d1 = new Date(this.range[0])
			var d2 = new Date(this.range[1])
			if (d1.getMonth() == d2.getMonth()) {
				if (d1.getDate() == d2.getDate()) {
					return (
						d1.getDate() +
						' ' +
						monthNames[d1.getMonth()] +
						' ' +
						d1.getFullYear()
					)
				}
				return (
					d1.getDate() +
					' - ' +
					d2.getDate() +
					' ' +
					monthNames[d1.getMonth()] +
					' ' +
					d1.getFullYear()
				)
			} else {
				return (
					d1.getDate() +
					' ' +
					monthNames[d1.getMonth()] +
					' - ' +
					d2.getDate() +
					' ' +
					monthNames[d2.getMonth()] +
					' ' +
					d1.getFullYear()
				)
			}
		}
	},

	methods: {
		fetchData() {
			axios
				.get(
					'http://127.0.0.1:5000/api/album_data/' +
						this.$route.query.album +
						'/l'
				)
				.then(response => {
					this.albums = response.data.albums
					this.photos = response.data.photos
					this.name = response.data.name
					this.range = response.data.range
					console.log(response, this.$route.query.album)
				})
				.catch(e => {
					console.log(e.message)
				})
		},
		change_name(new_name) {
			axios.post(
				'http://127.0.0.1:5000/api/update_album/' +
					this.$route.query.album,
				{ name: new_name }
			)
		},
		onScroll() {
			var offset = window.pageYOffset || document.documentElement.scrollTop
			if (offset > 400){
				this.toTop = true
			}
			else {
				this.toTop = false
			}
		}
	},

	created() {
		this.fetchData()
	}
}
</script>


<style>
.aspect-4x3 {
	flex-grow: 1.5 !important;
}

.aspect-3x4 {
	flex-grow: 0.85 !important;
}

.theme--light .toolbar {
	background-color: #fafafa;
}


#title {
	font-size: 56px;
	height: auto;
}

.input-group__input:hover + .input-group__details::before {
	background-color: rgba(0, 0, 0, 0.12) !important;
}

.input-group__details::before {
	background-color: transparent !important;
}

.theme--light .input-group.input-group--solo-inverted {
	background: rgba(255, 255, 255, 0.16);
}

.input-group__hint {
	font-size: 14px;
}

.input-group {
	padding-top: 0;
}

.theme--light .input-group.input-group--solo-inverted.input-group--focused {
	background: #d4d3d3;
}

.drop-enter-active,
.drop-leave-active {
	transition-property: transform;
	transition-duration: 0.5s;
}

.drop-enter,
.drop-leave-active {
	transform: translateY(80px)
}
</style>
