<template>
	<v-container grid-list-md v-scroll="onScroll">
		<v-toolbar light color="white" fixed flat app style="box-shadow: inset 0 -1px 0 0 rgba(0,0,0,0.12) !important;">
			<v-toolbar-title><img src="@/assets/logo.png" style="height: 1.5em; vertical-align: top;"/>Fetula
			</v-toolbar-title>
			<div class="search">
				<v-text-field
						prepend-icon="search"
						color="whitesmoke"
						flat
						label="Search"
						solo-inverted
						class="mx-3"
				></v-text-field>
			</div>
			<v-spacer></v-spacer>
			<v-tooltip bottom>
				<v-btn icon slot="activator" @click="process = true">
					<v-icon>toys</v-icon>
				</v-btn>
				<span>Process Photos</span>
			</v-tooltip>
			<v-tooltip bottom>

				<v-btn icon slot="activator" @click="athena">
					<v-badge color="red">
						<span slot="badge" v-if="notifications > 0">{{notifications}}</span>
						<img src="@/assets/athena.svg" style="height: 22px;"/>
					</v-badge>
				</v-btn>

				<span>Athena</span>
			</v-tooltip>
			<v-tooltip bottom>
				<v-btn icon slot="activator" @click="grid=!grid">
					<v-icon v-if="grid">view_agenda</v-icon>
					<v-icon v-else>view_module</v-icon>
				</v-btn>
				<span>Grid View</span>
			</v-tooltip>
			<v-tooltip bottom>
				<v-btn icon slot="activator">
					<v-icon>settings</v-icon>
				</v-btn>
				<span>Settings</span>
			</v-tooltip>
		</v-toolbar>
		<div>
			<v-content>
				<v-layout row wrap v-if="!grid">
					<album v-for="album in albums" :key="album" :albumid="album"/>
				</v-layout>
				<album-thumbnail v-else v-for="album in albums" :key="album" :albumid="album" :size="200"/>
			</v-content>
		</div>
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

		<v-dialog v-model="process" max-width="500px">
			<v-card>
				<v-card-text>
					<v-switch
							label="Scan folder structure"
							v-model="proc_conf.scan"
							disabled
					></v-switch>
					<v-switch
							label="Generate thumbnails"
							v-model="proc_conf.thumbnails"
					></v-switch>
					<v-switch
							label="Detect rotation"
							v-model="proc_conf.rotation"
					></v-switch>
					<v-switch
							label="Generate fuzzy hashes"
							v-model="proc_conf.hashes"
					></v-switch>
					<v-switch
							label="Find similar photos"
							v-model="proc_conf.similar"
					></v-switch>
					<v-switch
							label="Detect faces"
							v-model="proc_conf.faces"
					></v-switch>
					<v-switch
							label="Detect objects"
							v-model="proc_conf.objects"
					></v-switch>
					<v-checkbox
							label="Force"
							v-model="proc_conf.force"
					></v-checkbox>
				</v-card-text>
				<v-card-actions>
					<v-btn color="primary" flat @click.stop="process=false">Close</v-btn>
					<v-spacer></v-spacer>
					<v-btn color="primary" flat @click.stop="go_process">Apply</v-btn>
				</v-card-actions>
			</v-card>
		</v-dialog>
</v-container>
</template>

<script>
import Album from '@/components/Album.vue'
import AlbumThumbnail from '@/components/AlbumThumbnail.vue'
import axios from 'axios'

export default {
	name: 'home',
	components: {
		Album,
		AlbumThumbnail
	},

	data() {
		return {
			progress: 0,
			fetching: false,
			albums: [],
			toTop: false,
			grid: false,
			notifications: 0,
			process: false,
			proc_conf: {
				scan: true,
				thumbnails: false,
				rotation: false,
				hashes: false,
				similar: false,
				faces: false,
				objects: false,
				force: false
			}
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
					})
					.catch(e => {
						console.log(e.message)
					})

				axios
					.get('http://127.0.0.1:5000/api/home')
					.then(response => {
						this.fetching = false
						this.notifications = response.data.notifications
					})
					.catch(e => {
						console.log(e.message)
					})
			}
		},
		go_process() {
			this.$router.push({
				name: 'process',
				query: this.proc_conf
			})
		},
		athena() {
			this.$router.push({
				name: 'assistant',
			})
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
		this.fetchMeta()
	}
}
</script>

<style scoped>

.theme--light .input-group.input-group--solo-inverted {
    background: whitesmoke;
}

.theme--light .input-group.input-group--solo-inverted.input-group--focused {
    background: #d4d3d3;
}

.search {
	left: 50%;
    position: absolute;
    transform: translateX(-50%);
    width: 50%;
}

.toolbar__title {
	margin-left: 0 !important;
    left: 15%;
    position: absolute;
    transform: translateX(-50%);
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

.badge__badge {
	transform: scale(0.7) translateX(-8px) translateY(4px);
}
</style>
