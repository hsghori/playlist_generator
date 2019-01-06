# Spotify playlist generator

This is a django based single page web app that uses LastFM scrobble data to generate a playlist
baed on your most listened to tracks of the week. It requires a LastFM account and a spotify account
which has been linked to LastFM. 

## Development

The frontend is written in VueJS and the backend is written in Python (using Django). Currently no data
is stored in the backend though I plan to add some login / data storage functionality in the future
(for example to load previously generated playlists). 

You can install JS dependencies using npm and python dependencies using pipenv. 
