<template>
<v-container grid-list-md>
	<div style="padding-bottom: 4px">
		<v-text-field
        prepend-icon="search"
        label="Search"
        solo-inverted
        class="mx-3"
        
		style="width: 60%;
    left: 50%;
    transform: translateX(-50%);"
      ></v-text-field>
	</div>
    <v-layout row wrap>
      	<album v-for="album in albums" :key="album" :albumid="album"/>
    </v-layout>
</v-container>
</template>

<script>
import Album from '@/components/Album.vue'
import axios from 'axios'

export default {
	name: 'home',
	components: {
		Album
	},

	data() {
		return {
			progress: 0,
			fetching: false,
			albums: []
		}
	},

	methods: {
		fetchMeta() {
			if (this.fetching != true) {
				this.fetching = true
				axios
					.get('http://127.0.0.1:5000/api/albums')
					.then(response => {
						this.fetching = false
						this.albums = response.data
						console.log(this.albums)
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
