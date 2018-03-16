<template>
        <div style="padding:10px">
                    <v-card>
                        <v-card-title style="padding-bottom: 4px;"><h3>Tags</h3></v-card-title>
                    <v-select
                        style="box-shadow: none;"
                        chips
                        tags
                        solo
                        append-icon=""
                        v-model="data.tags">
                        <template slot="selection" slot-scope="data">
                        <v-chip
                            close
                            small
                            @input="remove(data.item)"
                            :selected="data.selected">
                            <strong>{{ data.item }}</strong>
                        </v-chip>
                        </template>
                    </v-select>
                    </v-card>
                    <br/>
                    <v-card>
                        <v-card-title style="padding-bottom: 4px;"><h3>People</h3></v-card-title>
                        <v-card-text style="padding-bottom: 8px; padding-top: 0;">
                        <v-avatar
                        :size="52"
                        class="grey lighten-4">
                        <img src="@/assets/logo.png" alt="avatar">
                        </v-avatar>
						<v-avatar
                        :size="52"
                        class="grey lighten-4">
                        <v-icon color="grey lighten-1" x-large>add</v-icon>
                        </v-avatar>
                        </v-card-text>
                    </v-card>
                    <br/>
					<v-card>
						<v-card-text style="padding-bottom: 0; padding-top: 0;">
						<v-list two-line subheader style="padding-bottom: 0;">
						<v-list-tile avatar inactive @click="" style="cursor: pointer">
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

export default {
	name: 'view-details',
	props: ['data'],
	components: {
		
	},
	data() {
		return {
			fetching: false,
		}
	},

	computed: {
		month() {
			var date = new Date(this.data.date)
			var monthNames = [
				"January", "February", "March",
				"April", "May", "June", "July",
				"August", "September", "October",
				"November", "December"
			];

			var monthIndex = date.getMonth()

			return monthNames[monthIndex];
		},

		date() {
			var date = new Date(this.data.date)
			return date.getDate()
		},

		day() {
			var date = new Date(this.data.date)
			var days = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"]

			return days[date.getDay()]
		},

		time() {
			var date = new Date(this.data.date)
			return date.getHours() + ":" + date.getMinutes()
		},

		albumImg() {
			return 'http://127.0.0.1:5000/api/image/' + this.data.album.id + '/A/s'
		},

		albumRange() {
			var monthNames = [
				"Jan", "Feb", "Mar",
				"Apr", "May", "Jun", "Jul",
				"Aug", "Sep", "Oct",
				"Nov", "Dec"
			];

			var d1 = new Date(this.data.album.range[0])
			var d2 = new Date(this.data.album.range[1])
			if (d1.getMonth() == d2.getMonth()){
				if (d1.getDate() == d2.getDate()){
					return d1.getDate() + " " + monthNames[d1.getMonth()] + " " + d1.getFullYear()
				}
				return d1.getDate() + " - " + d2.getDate() + " " + monthNames[d1.getMonth()] + " " + d1.getFullYear()
			}
			else {
				return d1.getDate() + " " + monthNames[d1.getMonth()] + " - " + d2.getDate() + " " + monthNames[d2.getMonth()] + " " + d1.getFullYear()
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
</style>
