
<template>
	<div class="wrapper">
		<v-tooltip bottom>
			<v-avatar
			slot="activator"
			:size="52"
			class="grey lighten-4"
			v-on:mouseover="mouseOver"
			v-on:mouseout="mouseOut"
			style="cursor: pointer"
			@click="activate">
			<img v-if="person.name != '%add'" :src="source" alt="avatar" @contextmenu="show">
			<v-icon v-else color="grey lighten-1" x-large @click.stop="edit = true">add</v-icon>
			</v-avatar>
			<span>{{person.name != '%add' ? person.name : 'Add Person'}}</span>
		</v-tooltip>
		<v-dialog v-model="edit" max-width="500px">
			<v-card>
			<v-card-text>
				<v-select
				:items="names"
				v-model="name"
				label="Name"
				autocomplete
				></v-select>
			</v-card-text>
			<v-card-actions>
				<v-btn color="primary" flat @click.stop="edit=false">Close</v-btn>
				<v-spacer></v-spacer>
				<v-btn v-if="person.name != '%add'" color="primary" flat @click.stop="del">Delete</v-btn>
				<v-btn color="primary" flat @click.stop="apply">Apply</v-btn>
			</v-card-actions>
			</v-card>
		</v-dialog>
	</div>
</template>

<script>
//top, right, bottom, left
import { EventBus } from '@/event_bus.js'
import axios from 'axios'

export default {
	name: 'Person',
	props: ['person', 'data'],
	data() {
		return {
			edit: false,
			names: [],
			name: this.person.name
		}
	},

	computed: {
		source() {
			return 'http://127.0.0.1:5000/api/person_image/' + this.person.name
		}
	},

	methods: {
		activate() {
			this.$router.push({
				name: 'person',
				query: { name: this.person.name }
			})
		},
		mouseOver() {
			EventBus.$emit('face-hover', this.person.name)
		},
		mouseOut() {
			EventBus.$emit('face-out', this.person.name)
		},
		getNames() {
			axios
				.get('http://127.0.0.1:5000/api/person_names')
				.then(response => {
					this.names = response.data.names
				})
				.catch(e => {
					console.log(e.message)
				})
		},
		show(e) {
			e.preventDefault()
			this.edit = false
			this.$nextTick(() => {
				this.edit = true
			})
		},
		apply(){
			this.edit = false
			if (this.person.name == "%add"){
				axios.post(
					'http://127.0.0.1:5000/api/update_image/' +
					this.data.id,
					{ addPerson: {name: this.name} }
				)
				this.data.people.push({'name': this.name, 'position': [0, 0, 0, 0]})
				this.name = "%add"
			}
			else {
				axios.post(
					'http://127.0.0.1:5000/api/update_image/' +
					this.data.id,
					{ changePerson: {oldName: this.person.name, newName:this.name} }
				)
				this.person.name = this.name
			}

		},
		del(){
			this.edit = false
			axios.post(
				'http://127.0.0.1:5000/api/update_image/' +
				this.data.id,
				{ delPerson: {name: this.name} }
			)
			this.data.people.splice( this.data.people.indexOf(this.person), 1 )
		}
	},
	created() {
		this.getNames()
	}
}
</script>

<style scoped>
.fade {
	opacity: 0.6;
}
.wrapper {
	display: inline-block;
	margin-right: 5px;
}
</style>
