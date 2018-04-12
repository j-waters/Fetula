<template>
	<v-select
			style="box-shadow: none;"
			chips
			tags
			solo
			append-icon=""
			v-model="tags"
			:items="names"
			@change="updateTags"
			@input="updateTags"
			autocomplete>
		<template slot="selection" slot-scope="data">
			<v-tooltip bottom>
				<v-chip
						slot="activator"
						small
						close
						:selected="data.selected"
						@input="del(data.item)"
						v-on:mouseover="mouseOver(data)"
						v-on:mouseout="mouseOut(data)">
					<strong>{{ data.item }}</strong>
				</v-chip>
				<span>{{ confidence(data.item) }}</span>
			</v-tooltip>
		</template>
	</v-select>
</template>

<script>
//top, right, bottom, left
import { EventBus } from '@/event_bus.js'
import axios from 'axios'

export default {
	name: 'Tags',
	props: ['data'],
	data() {
		let tags = this.data.tags.map(function(item){
			return item.name
		})
		return {
			names: [],
			tags: tags.filter(function(item, index, array){
				return array.indexOf(item) == index
			})
		}
	},

	watch: {
		'data.tags': function() {
			let tags = this.data.tags.map(function(item){
				return item.name
			})
			this.tags = tags.filter(function(item, index, array){
				return array.indexOf(item) == index
			})
		}
	},

	methods: {
		confidence(item) {
			if (!item) return '---'
			var out = ''
			for (var i in this.data.tags){
				if (this.data.tags[i].name == item){
					if (out != ''){
						out += ' / '
					}
					out += this.data.tags[i].confidence + '%'
				}
			}
			if (out == '') {
				return '100%'
			}
			return out
		},
		mouseOver(data) {
			EventBus.$emit('detected-hover', data.item)
		},
		mouseOut(data) {
			EventBus.$emit('detected-out', data.item)
		},
		getTags() {
			axios
				.get('http://127.0.0.1:5000/api/tag_names')
				.then(response => {
					this.names = response.data.names
				})
				.catch(e => {
					console.log(e.message)
				})
		},
		
		updateTags(){
			this.data.tags = this.data.tags.filter(function(item){
				return this.tags.includes(item.name)
			}.bind(this))
			axios.post(
				'http://127.0.0.1:5000/api/update_image/' +
				this.data.id,
				{ tags: this.tags }
			)
		},
		del(item){
			this.tags.splice( this.tags.indexOf(item), 1 )
			this.updateTags()
		}
	},
	created() {
		this.getTags()
	},
}


</script>

<style scoped>
</style>
