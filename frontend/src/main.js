import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import VueClazyLoad from 'vue-clazy-load'
import ProgressiveImage from 'progressive-image/dist/vue'

Vue.use(ProgressiveImage, {
	removePreview: true,
  });


Vue.use(VueClazyLoad)

Vue.use(Vuetify)

Vue.config.productionTip = false

new Vue({
	router,
	store,
	render: h => h(App)
}).$mount('#app')
