from random import shuffle
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOauthError


def create_playlist(token, playlist_name='test'):
    if not token:
        return {'error': 'Invalid token'}

    try:
        spotify = Spotify(auth=token)
        spotify_username = spotify.current_user().get('id', None)
    except SpotifyOauthError as e:
        return {'error': str(e)}
    if not spotify_username:
        return {'error': 'Could not find spotify user'}

    top_tracks = spotify.current_user_top_tracks(
        time_range='short_term').get("items", [])
    base_artist_ids = {
        artist["id"] for track in top_tracks for artist in track["artists"]
    }
    artist_ids = set()
    for artist_id in base_artist_ids:
        artists = spotify.artist_related_artists(artist_id).get("artists", [])
        artist_ids = artist_ids.union(set([
            artist["id"] for artist in artists[:5]
        ]))

    potential_tracks = {}
    for artist_id in artist_ids:
        tracks = spotify.artist_top_tracks(artist_id).get("tracks", [])
        potential_tracks.update({
            track["uri"]: track for track in tracks[:5]
        })

    playlist_track_uris = list(potential_tracks.keys())
    shuffle(playlist_track_uris)
    playlist_track_uris = playlist_track_uris[:100]
    playlist_track_info = []
    for uri in playlist_track_uris:
        track = potential_tracks[uri]
        playlist_track_info.append({
            'title': track['name'],
            'artists': ', '.join([artist['name'] for artist in track['artists']]),
            'link': track['external_urls']['spotify'],
            'image': track['album']['images'][0]
        })

    playlist = spotify.user_playlist_create(
        spotify_username, playlist_name, public=False)
    spotify.user_playlist_add_tracks(
        spotify_username, playlist["id"], playlist_track_uris)
    return {
        'url': playlist['external_urls'].get('spotify'),
        'name': playlist.get('name'),
        'track_info': playlist_track_info
    }
