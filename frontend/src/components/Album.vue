<template>
        <v-flex xs12>
        <v-card hover>
          <v-card-title @click="activate"><h3 style="font-weight: 400;">{{name}}</h3> <v-chip disabled>{{size}} {{(size == 1) ? "photo" : "photos"}}</v-chip><span class="grey--text">{{albumRange}}</span><br></v-card-title>
					<v-card-text>
            <album-thumbnail v-for="album in subAlbums" :albumid="album" :key="album"/>
            <thumbnail v-for="photo in photos" :key="photo" :photoid="photo" :album="albumid" :size="128"/>
          </v-card-text>
        </v-card>
      </v-flex>
</template>

<script>
// TODO: Seperate album metadata get
import Thumbnail from '@/components/Thumbnail.vue'
import AlbumThumbnail from '@/components/AlbumThumbnail.vue'
import axios from 'axios'

export default {
	name: 'Album',
	props: ['albumid'],
	components: {
		Thumbnail,
		AlbumThumbnail
	},
	data() {
		return {
			photos: [],
			subAlbums: [],
			size: 0,
			name: '',
			fetching: false,
			range: [0, 0]
		}
	},
	methods: {
		fetchMeta() {
			if (this.fetching != true) {
				this.fetching = true
				axios
					.get('http://127.0.0.1:5000/api/album_data/' + this.albumid)
					.then(response => {
						this.fetching = false
						this.photos = response.data.highlights
						this.subAlbums = response.data.albums
						this.size = response.data.size
						this.name = response.data.name
						this.range = response.data.range
					})
					.catch(e => {
						console.log(e.message)
					})
			}
		},

		activate() {
			console.log("click", this.albumid)
			this.$router.push({
				name: 'album',
				query: { album: this.albumid }
			})
		}
	},

	computed: {
		albumRange() {
			var monthNames = [
				"Jan", "Feb", "Mar",
				"Apr", "May", "Jun", "Jul",
				"Aug", "Sep", "Oct",
				"Nov", "Dec"
			];

			var d1 = new Date(this.range[0])
			var d2 = new Date(this.range[1])
			if (d1.getMonth() == d2.getMonth()){
				if (d1.getDate() == d2.getDate()){
					return d1.getDate() + " " + monthNames[d1.getMonth()] + " " + d1.getFullYear()
				}
				return d1.getDate() + " - " + d2.getDate() + " " + monthNames[d1.getMonth()] + " " + d1.getFullYear()
			}
			else {
				return d1.getDate() + " " + monthNames[d1.getMonth()] + " - " + d2.getDate() + " " + monthNames[d2.getMonth()] + " " + d1.getFullYear()
			}
		}
	},

	created() {
		this.fetchMeta()
	}
}
</script>

<style scoped lang="css">
.card__title {
  padding-bottom: 0
}
</style>
