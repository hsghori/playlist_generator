from random import shuffle
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOauthError
from playlist_generator.utils.lastfm import LastFM


def get_playlist_tracks(last_fm_key, lastfm_username):
    lfm = LastFM(last_fm_key)
    tracks = lfm.get_user_top_tracks(lastfm_username, limit=10, period='7day')
    exclusion_artists = {
        artist['name']
        for artist in lfm.get_top_artists(lastfm_username, keys=['name'], limit=100)
        if 'error' not in artist
    }
    top_artists, playlist = set(), set()
    for track in tracks:
        if 'error' not in track:
            artists = [
                artist['name']
                for artist in lfm.get_similar_artists(track['artist']['name'], keys=['name'], limit=10)
                if 'error' not in artist
            ]
            top_artists.update(
                {artist for artist in artists if artist not in exclusion_artists}
            )
    for artist in top_artists:
        tracks = [
            track['name']
            for track in lfm.get_top_tracks_by_artist(artist, keys=['name'], limit=2)
            if 'error' not in track
        ]
        playlist.update(tracks)
    return list(playlist)


def create_playlist(token, track_titles, playlist_name='test'):
    if not token:
        return {'error': 'Invalid token'}

    try:
        spotify = Spotify(auth=token)
        spotify_username = spotify.current_user().get('id', None)
    except SpotifyOauthError as e:
        return {'error': str(e)}
    if not spotify_username:
        return {'error': 'Could not find spotify user'}

    playlist = spotify.user_playlist_create(
        spotify_username, playlist_name, public=False)
    playlist_id = playlist['id']
    track_uris = []
    shuffle(track_titles)
    track_titles = track_titles[:100] \
        if len(track_titles) > 100 \
        else track_titles
    playlist_track_info = []
    for track in track_titles:
        track_dict = spotify.search(track, limit=1, type='track')
        is_valid_track = (
            'tracks' in track_dict and
            'items' in track_dict['tracks'] and
            len(track_dict['tracks']['items']) > 0 and
            'uri' in track_dict['tracks']['items'][0]
        )
        if is_valid_track:
            valid_track_dict = track_dict['tracks']['items'][0]
            track_uris.append(valid_track_dict['uri'])
            playlist_track_info.append({
                'title': valid_track_dict['name'],
                'artists': ', '.join([artist['name'] for artist in valid_track_dict['artists']]),
                'link': valid_track_dict['external_urls']['spotify'],
                'image': valid_track_dict['album']['images'][0]
            })
    spotify.user_playlist_add_tracks(spotify_username, playlist_id, track_uris)
    return {
        'url': playlist['external_urls'].get('spotify'),
        'name': playlist.get('name'),
        'track_info': playlist_track_info
    }
