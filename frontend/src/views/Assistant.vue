<template>
	<v-container grid-list-md v-scroll="onScroll">
		<v-toolbar light color="white" fixed flat app style="box-shadow: inset 0 -1px 0 0 rgba(0,0,0,0.12) !important;">
			<v-toolbar-title style="left: 50% !important;"><img src="@/assets/athena.svg"
																style="height: 1.5em; vertical-align: top"/>thena
			</v-toolbar-title>
			<v-btn icon @click="$router.go(-1)">
				<v-icon>arrow_back</v-icon>
			</v-btn>
		</v-toolbar>
		<v-content>
			<v-layout row wrap>
				<similar v-for="s in similar" :key="'s' + similar.indexOf(s)" :suggestion="s"/>
				<rotation v-for="r in rotations" :key="'r' + rotations.indexOf(r)" :suggestion="r"/>
			</v-layout>
		</v-content>

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
	</v-container>
</template>

<script>
import Similar from '@/components/Similar.vue'
import Rotation from '@/components/Rotation.vue'
import axios from 'axios'

export default {
	name: 'assistant',
	components: {
		Similar,
		Rotation
	},

	data() {
		return {
			similar: [],
			rotations: [],
			toTop: false
		}
	},

	methods: {
		fetchMeta() {
			if (this.fetching != true) {
				this.fetching = true
				axios
					.get('http://127.0.0.1:5000/api/assistant')
					.then(response => {
						this.fetching = false
						this.similar = response.data.similar
						this.rotations = response.data.rotations
					})
					.catch(e => {
						console.log(e.message)
					})
			}
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
