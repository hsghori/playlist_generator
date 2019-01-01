let $ = require('jquery');
let axios = require('axios');
let { box, stop } = require('styledot/loading');
let Vue = require('vue');


Vue.component('combined-form-input', {
	delimiters: ['[[', ']]'],
	props: {
		input_id: String,
		input_label: String, 
		input_invalid_message: String,
		input_type: String,
		value: String
	},
	data: function() {
		return {
			is_invalid: false,
		};
	},
	methods: {
		validateAndEmit: function(event) {
			this.$emit('input', event.target.value);
			this.is_invalid = !event.target.value;
		},
	},
	template: `
		<div class='combined-form-input'>
			<label v-bind:for="[[ input_id ]]">
				[[ input_label ]]
			</label>
			<input 
				v-bind:value="[[ value ]]"
				v-on:input="validateAndEmit" 
				v-bind:class="{ 'mod-invalid': is_invalid }"
				v-bind:placeholder="[[ input_label ]]" 
				v-bind:id="[[ input_id ]]" 
				class="sd-form-input"
				v-bind:type="[[ input_type ]]">
			<div class="sd-form-error-msg" v-bind:class="{ hide: is_invalid }">
				[[ input_invalid_message ]]
			</div>
		</div>
	`
});

if (!spotify_token) {
	let authApp = new Vue({
		delimiters: ['[[', ']]'],
		el: '#auth-module',
		data: {
			spotify_auth_link: '',
		},
	});
	axios.get('/auth_spotify/').then(
		(response) => {
			authApp.spotify_auth_link = response.data.spotify_auth_url;
		}
	);
} else {
	let mainApp = new Vue({
		delimiters: ['[[', ']]'],
		el: '#info-module',
		data: {
			spotify_token: spotify_token,
			lastfm_username: '',
			playlist_name: '',
			lastfm_username_input: {
				input_label: 'LastFM username',
				input_invalid_message: 'Invalid LastFM username',
				input_id: 'lastfm_username_input',
				input_type: 'text',
				value: '',
			},
			playlist_name_input: {
				input_label: 'Playlist name',
				input_invalid_message: 'Invalid playlist name',
				input_id: 'playlist_name_input',
				input_type: 'text',
				value: '',
			},
		},
		methods: {
			submitForm: function() {
				if (this.lastfm_username && this.playlist_name) {
					box($('#info-module'), 'Loading');
					axios.get(
						'/create_playlist/', {
						params: {
							lastfm_username: this.lastfm_username,
							playlist_name: this.playlist_name,
							spotify_token: this.spotify_token,
						}
					}).then((response) => {
						stop($('#info-module'));
					}).catch((error) => {
						console.log(error);
						stop($('#info-module'));
					});
				}
			},
			validateLastFmUsername: function() {
				this.lastfm_username_input_invalid = !this.lastfm_username;
			},
			validatePlaylistName: function() {
				this.playlist_input_invalid = !this.playlist_name;
			},
		},
	});
}
