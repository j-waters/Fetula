import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import VueClazyLoad from 'vue-clazy-load'
import VueProgressiveImage from 'vue-progressive-image'
//Vue.use(require('vue-masonry').VueMasonryPlugin);
import vuescroll from 'vue-scroll'

Vue.use(vuescroll, {throttle: 600})

Vue.use(VueProgressiveImage)


Vue.use(VueClazyLoad)

Vue.use(Vuetify)

Vue.config.productionTip = false

new Vue({
	router,
	store,
	render: h => h(App)
}).$mount('#app')
