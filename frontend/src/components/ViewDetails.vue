<template>
        <div style="padding:10px">
                    <v-card>
						<v-card-title style="padding-bottom: 4px;"><h3>Tags</h3>
							<v-btn icon @click="genTags">
								<v-icon small style="color: #555" :class="{'spin': fetchTags}">sync</v-icon>
							</v-btn>
						</v-card-title>
						<tags :data="data"/>
                    </v-card>
                    <br v-if="data.people.length > 0"/>
                    <v-card v-if="data.people.length > 0">
                        <v-card-title style="padding-bottom: 4px;"><h3>People</h3></v-card-title>
                        <v-card-text style="padding-bottom: 8px; padding-top: 0;">
                        <person v-for="person in data.people" :key="person.name" :person="person" :data="data"/>
						<person :key="'add'" :person="{name: '%add'}" :data="data"/>
                        </v-card-text>
                    </v-card>
                    <br/>
					<v-card>
						<v-card-text style="padding-bottom: 0; padding-top: 0;">
						<v-list two-line subheader style="padding-bottom: 0;">
						<v-list-tile avatar inactive v-on:click.native.stop="goAlbum" style="cursor: pointer">
                                    <v-list-tile-avatar>
                                        <v-avatar
										tile
										:size="36"
										class="grey lighten-4">
										<img :src="albumImg" alt="avatar">
										</v-avatar>
                                    </v-list-tile-avatar>
                                    <v-list-tile-content>
                                        <v-list-tile-title>{{data.album.path}}</v-list-tile-title>
                                        <v-list-tile-sub-title>{{data.album.size}} items · {{albumRange}}</v-list-tile-sub-title>
                                    </v-list-tile-content>
                                </v-list-tile>
						</v-list>
						</v-card-text>
					</v-card>
					<br/>
                    <v-card>
                        <v-card-title style="padding-bottom: 0;"><h3>Details</h3></v-card-title>
                        <v-card-text style="padding-bottom: 0; padding-top: 0;">
                            <v-list two-line subheader style="padding-bottom: 0;">
                                <v-list-tile avatar @click="">
                                    <v-list-tile-avatar>
                                        <v-icon medium>today</v-icon>
                                    </v-list-tile-avatar>
                                    <v-list-tile-content>
                                        <v-list-tile-title>{{date}} {{month}}</v-list-tile-title>
                                        <v-list-tile-sub-title>{{day}}, 14:56</v-list-tile-sub-title>
                                    </v-list-tile-content>
                                    <v-list-tile-action>
                                        <v-icon color="grey lighten-1">edit</v-icon>
                                    </v-list-tile-action>
                                </v-list-tile>
                                
                                <v-list-tile avatar>
                                    <v-list-tile-avatar>
                                        <v-icon medium>photo</v-icon>
                                    </v-list-tile-avatar>
                                    <v-list-tile-content>
                                        <v-list-tile-title>{{data.name}}</v-list-tile-title>
                                        <v-list-tile-sub-title style="font-size: 12px;">{{data.mp}} MP &thinsp; {{data.width}} × {{data.height}} &thinsp; {{Math.round(data.size / 1048576, 2)}} MB</v-list-tile-sub-title>
                                    </v-list-tile-content>
                                </v-list-tile>

                                <v-list-tile avatar>
                                    <v-list-tile-avatar>
                                        <v-icon medium>camera</v-icon>
                                    </v-list-tile-avatar>
                                    <v-list-tile-content>
                                        <v-list-tile-title>{{data.make}} {{data.model}}</v-list-tile-title>
                                        <v-list-tile-sub-title style="font-size: 12px;">f/{{data.fstop}} &thinsp; {{data.exposure}} &thinsp; {{data.flength}} mm &thinsp; ISO{{data.ISOspeed}}</v-list-tile-sub-title>
                                    </v-list-tile-content>
                                </v-list-tile>

                                <v-list-tile avatar>
                                    <v-list-tile-avatar>
                                        <v-icon medium>location_on</v-icon>
                                    </v-list-tile-avatar>
                                    <v-list-tile-content>
                                        <v-list-tile-title>Bath</v-list-tile-title>
                                        <v-list-tile-sub-title style="font-size: 12px;">36.113, -115.175</v-list-tile-sub-title>
                                    </v-list-tile-content>
                                </v-list-tile>
								
                            </v-list>
                        </v-card-text>
                    </v-card>
                </div>
</template>

<script>
import axios from 'axios'
import Person from '@/components/Person.vue'
import Tags from '@/components/Tags.vue'
import { EventBus } from '@/event_bus.js'

export default {
	name: 'view-details',
	props: ['data'],
	components: {
		Person,
		Tags
	},
	data() {
		return {
			fetching: false,
			fetchTags: false,
			fetchPerson: false
		}
	},
	methods: {
		goAlbum() {
			this.$router.push({
				name: 'album',
				query: { album: this.data.album.id }
			})
		},
		genTags() {
			this.fetchTags = true
			axios
				.get(
					'http://127.0.0.1:5000/api/gen_image/' +
						this.$route.query.photo +
						'/tags'
				)
				.then(response => {
					this.data.tags = response.data
					this.fetchTags = false
					console.log('fetched', this.data.tags)
				})
				.catch(e => {
					console.log(e.message)
				})
		}
	},

	computed: {
		month() {
			var date = new Date(this.data.date)
			var monthNames = [
				'January',
				'February',
				'March',
				'April',
				'May',
				'June',
				'July',
				'August',
				'September',
				'October',
				'November',
				'December'
			]

			var monthIndex = date.getMonth()

			return monthNames[monthIndex]
		},

		date() {
			var date = new Date(this.data.date)
			return date.getDate()
		},

		day() {
			var date = new Date(this.data.date)
			var days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat']

			return days[date.getDay()]
		},

		time() {
			var date = new Date(this.data.date)
			return date.getHours() + ':' + date.getMinutes()
		},

		albumImg() {
			return (
				'http://127.0.0.1:5000/api/image/' +
				this.data.album.cover +
				'/s'
			)
		},

		albumRange() {
			var monthNames = [
				'Jan',
				'Feb',
				'Mar',
				'Apr',
				'May',
				'Jun',
				'Jul',
				'Aug',
				'Sep',
				'Oct',
				'Nov',
				'Dec'
			]

			var d1 = new Date(this.data.album.range[0])
			var d2 = new Date(this.data.album.range[1])
			if (d1.getMonth() == d2.getMonth()) {
				if (d1.getDate() == d2.getDate()) {
					return (
						d1.getDate() +
						' ' +
						monthNames[d1.getMonth()] +
						' ' +
						d1.getFullYear()
					)
				}
				return (
					d1.getDate() +
					' - ' +
					d2.getDate() +
					' ' +
					monthNames[d1.getMonth()] +
					' ' +
					d1.getFullYear()
				)
			} else {
				return (
					d1.getDate() +
					' ' +
					monthNames[d1.getMonth()] +
					' - ' +
					d2.getDate() +
					' ' +
					monthNames[d2.getMonth()] +
					' ' +
					d1.getFullYear()
				)
			}
		}
	}
}
</script>

<style scoped lang="css">

h1,
h2,
h3,
h4,
h5,
h6 {
	font-weight: 400;
	line-height: 1.25;
	margin: 0 0 0.2em 0;
	color: #555;
}

.spin {
	animation: rot 2s infinite linear;
}

@keyframes rot {
    0% {
        -webkit-transform: rotate(0deg);
        transform: rotate(0deg)
    }

    to {
        -webkit-transform: rotate(1turn);
        transform: rotate(1turn)
    }
}
</style>
