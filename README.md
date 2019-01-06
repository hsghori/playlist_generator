# Spotify playlist generator

This is a django based single page web app that uses LastFM scrobble data to generate a playlist
baed on your most listened to tracks of the week. It requires a LastFM account and a spotify account
which has been linked to LastFM. 

If you want to run this locally you will need to create LastfM and Spotify apps
- [Create LastFM app](https://www.last.fm/api)
- [Create Spotify app](https://developer.spotify.com/)

Then create a file `/playlist_generator/utils/constants.py` of the form:

```Python
LASTFM_API_KEY = 'YOUR API KEY'
SPOTIFY_API_KEY = 'YOUR API KEY'
SPOTIFY_API_SECRET = 'YOUR SECRET KEY'
SPOTIFY_REDIRECT_URL = 'http://127.0.0.1:8000/'
```

## Development

The frontend is written in VueJS and the backend is written in Python (using Django). Currently no data
is stored in the backend though I plan to add some login / data storage functionality in the future
(for example to load previously generated playlists). 

You can install JS dependencies using npm and python dependencies using pipenv. 
