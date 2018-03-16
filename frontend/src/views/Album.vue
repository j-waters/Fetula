<template>
<v-container grid-list-md>
    <album-thumbnail v-for="album in albums" :albumid="album" :key="'a' + album"/>
            <thumbnail v-for="photo in photos" :key="photo" :photoid="photo" :album="$route.query.album" :size="256"/>

</v-container>
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
			fetching: false,
			albums: [],
			photos: []
		}
	},

	methods: {
		fetchMeta() {
			if (this.fetching != true) {
				this.fetching = true
				axios
					.get('http://127.0.0.1:5000/api/album_data/' + this.$route.query.album)
					.then(response => {
						this.fetching = false
						this.albums = response.data.albums
						this.photos = response.data.photos
						console.log(this.photos)
					})
					.catch(e => {
						console.log(e.message)
					})
			}
		}
	},

	created() {
		this.fetchMeta()
	}
}
</script>

<style>

.theme--light .input-group.input-group--solo-inverted {
    background: rgba(255,255,255, .16);
}

.theme--light .input-group.input-group--solo-inverted.input-group--focused {
    background: #d4d3d3;
}

</style>
