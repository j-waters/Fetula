import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import View from './views/View.vue'
import Album from './views/Album.vue'
import Person from './views/Person.vue'
import Process from './views/Process.vue'
import Assistant from './views/Assistant.vue'

Vue.use(Router)

export default new Router({
	mode: 'history',
	routes: [
		{
			path: '/',
			name: 'home',
			component: Home
		},
		{
			path: '/process',
			name: 'process',
			component: Process,
			props: true
		},
		{
			path: '/assistant',
			name: 'assistant',
			component: Assistant
		},
		{
			path: '/view',
			name: 'view',
			component: View,
			props: true
		},
		{
			path: '/album',
			name: 'album',
			component: Album,
			props: true
		},
		{
			path: '/person',
			name: 'person',
			component: Person,
			props: true
		}
	]
})
