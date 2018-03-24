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
<v-container>
	<v-layout row>
		<v-text-field
          name="input-1"
          id="title"
		  persistent-hint
		  :value="name"
		  @input="change_name"
        ></v-text-field>
	</v-layout>
	<v-layout row wrap>
        <thumbnail v-for="photo in photos" :key="photo" :photoid="photo" :size="256" :flex="true"/>
	</v-layout>
</v-container>
</div>
</template>

<script>
import Thumbnail from '@/components/Thumbnail.vue'
import axios from 'axios'

export default {
	name: 'home',
	components: {
		Thumbnail,
	},

	data() {
		return {
			photos: [],
			name: this.$route.query.name,
			id: null
		}
	},
	watch: {
		// call again the method if the route changes
		'$route': 'fetchData'
	},

	methods: {
		fetchData() {
			axios
				.get(
					'http://127.0.0.1:5000/api/person_data/' +
						this.$route.query.name
				)
				.then(response => {
					this.photos = response.data.photos
					this.id = response.data.id
				})
				.catch(e => {
					console.log(e.message)
				})
		},
		change_name(new_name) {
			axios.post(
				'http://127.0.0.1:5000/api/update_person/' +
					this.id,
				{ name: new_name }
			)
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
</style>
