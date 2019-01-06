import json
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from spotipy import oauth2
from datetime import datetime

from playlist_generator.utils.constants import (
    SPOTIFY_API_KEY, SPOTIFY_API_SECRET, SPOTIFY_REDIRECT_URL)
from playlist_generator.utils.playlist_creation_utils import get_playlist_tracks, create_playlist

SPOTIFY_SCOPES = ' '.join([
    'user-read-email',
    'playlist-read-private',
    'playlist-modify-private',
    'playlist-modify-public',
])


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        sp_oauth = oauth2.SpotifyOAuth(SPOTIFY_API_KEY, SPOTIFY_API_SECRET, SPOTIFY_REDIRECT_URL,
                                       scope=SPOTIFY_SCOPES)

        last_auth_time = self.request.session.get('last_auth')
        if not last_auth_time:
            self.request.session.flush()

        last_auth_time = datetime.strptime(last_auth_time, '%Y-%m-%d %H:%M:%S')
        time_diff = (datetime.now() - last_auth_time).total_seconds() / 3600
        if time_diff >= 1:
            self.request.session.flush()

        code = self.request.GET.get('code')
        token = self.request.session.get('token')
        context_data = {}
        if code and not token:
            token = sp_oauth.get_access_token(code)['access_token']
        if token:
            context_data = {
                'spotify_token': token
            }
            self.request.session['token'] = token
        return context_data


class PlaylistGenerateView(View):

    def post(self, request):
        params = json.loads(request.body).get('params')
        lastfm_username = params.get('lastfm_username')
        playlist_name = params.get('playlist_name')
        spotify_token = (params.get('spotify_token') or
                         request.session.get('token'))
        if not (lastfm_username and playlist_name and spotify_token):
            error_message = 'Bad request\nLastFM Username: %s\nPlaylist Name: %s\nSpotify token%s' % (
                lastfm_username, playlist_name, spotify_token)
            print error_message
            return JsonResponse({'error': error_message}, status=400)
        print lastfm_username, playlist_name, spotify_token
        playlist_tracks = get_playlist_tracks(lastfm_username)
        print playlist_tracks
        playlist_response = create_playlist(spotify_token, playlist_tracks)
        print playlist_response
        if 'error' in playlist_response:
            return JsonResponse(playlist_response, 500)
        return JsonResponse({'playlist': playlist_response})


class AuthSpotifyView(View):

    def get(self, request):
        sp_oauth = oauth2.SpotifyOAuth(SPOTIFY_API_KEY, SPOTIFY_API_SECRET, SPOTIFY_REDIRECT_URL,
                                       scope=SPOTIFY_SCOPES)
        auth_url = sp_oauth.get_authorize_url()
        request.session['last_auth'] = datetime.now(
        ).strftime('%Y-%m-%d %H:%M:%S')
        return JsonResponse({'spotify_auth_url': auth_url})
