<template>
	<v-container>
		<v-btn icon @click="es.close(); $router.go(-1)" style="display: block">
			<v-icon>arrow_back</v-icon>
		</v-btn>
		<img :src="source"/>
		<v-progress-linear :value="done / count * 100" height="40" color="info"></v-progress-linear>
		<!--span>Image {{id}} of {{count}}. Average time per image: {{Math.round(averageTime, 2)}} seconds. Predicted time till next image: {{Math.round(countdown)}} seconds. Total time left: {{Math.round(averageTime * (count-id) / 60)}} minutes ({{Math.round(averageTime * (count-id) / 60 / 60)}} hours)</span-->
		<span>Completed: {{done}} of {{count}}. Average time per image: {{Math.round(averageTime, 2)}} seconds. Predicted time till next chunk: {{Math.round(countdown)}} seconds. Total time left: {{Math.round(averageTime * (count-id) / 60)}} minutes ({{Math.round(averageTime * (count-id) / 60 / 60)}} hours)</span>
		<!--h3>Similar: {{similar}}</h3-->
		<div v-show="people.length != 0" style="width: 45%; margin-right: 10%; display: inline-block;">
			<h2>People</h2>
			<v-list>
				<template v-for="(item, index) in people">
					<v-list-tile-content :key='index'>
						<v-list-tile-title>{{item.name}}</v-list-tile-title>
						<v-list-tile-sub-title>{{item.confidence}}%</v-list-tile-sub-title>
					</v-list-tile-content>
				</template>
			</v-list>
		</div>
		<div v-show="tags.length != 0" style="width: 45%; display: inline-block;">
			<h2>Tags</h2>
			<v-list>
				<template v-for="(item, index) in tags">
					<v-list-tile-content :key='index'>
						<v-list-tile-title>{{item.name}}</v-list-tile-title>
						<v-list-tile-sub-title>{{item.confidence}}%</v-list-tile-sub-title>
					</v-list-tile-content>
				</template>
			</v-list>
		</div>
	</v-container>
</template>

<script>
export default {
	name: 'process',
	components: {
	},

	data() {
		return {
			id: 1,
			done: 0,
			count: 0,
			people: [],
			tags: [],
			//times: [],
			time: 0,
			similar: 0,
			countdown: 0,
		}
	},
	computed: {
		source() {
			if (this.averageTime < 3){
				return ""
			}
			return 'http://127.0.0.1:5000/api/image/' + this.id + '/m'
		},
		averageTime() {
			/*var sum = 0
			var len = this.times.length
			for( var i = 0; i < this.times.length; i++ ){
				if (this.times[i] > 10 || true){
					sum += this.times[i]
				}
				else {
					len -= 1
				}
			}

			var avg = sum/len
			return avg*/
			return this.time / this.done
		}
	},

	methods: {
		begin() {
			this.es = new EventSource('http://127.0.0.1:5000/api' + this.$route.fullPath)

			setInterval(function(){
				this.countdown += -1
			}.bind(this), 1000)

			this.es.addEventListener('message', event => {
				if (event.data == "STOP"){
					this.es.close()
					this.$router.go(-1)
					return
				}
				let data = JSON.parse(event.data)
				//this.id = data.id
				this.done = data.done
				this.count = data.count
				this.time = data.time
				this.countdown = this.averageTime * 4
				//this.times.push(data.time)
				/*this.people = data.people
				this.tags = data.tags
				this.times.push(data.time)
				this.countdown = this.averageTime
				self.similar = data.similar*/
			}, false)

			this.es.onerror = function() {
				if (this.es){
					this.es.close()
					this.$router.go(-1)
				}
			}
		}
	},
	beforeDestroy() {
		if (this.es){
			this.es.close()
		}
	},

	mounted() {
		this.begin()
	}
}


</script>

<style scoped>

img {
	position: relative;
    left: 50%;
    transform: translateX(-50%);
    max-width: 90%;
}

span {
	position: relative;
    left: 50%;
    text-align: center;
    vertical-align: middle;
    line-height: 40px;
    transform: translateX(-50%);
    display: block;
    top: -54.5px;
	z-index: 99;
}

h3 {
	text-align: center;
    position: relative;
    top: -40px;
}



</style>
