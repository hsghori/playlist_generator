from django.views.generic import View, TemplateView
from django.http import JsonResponse
from spotipy import oauth2
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
        code = self.request.GET.get('code')
        token = self.request.session.get('token')
        context_data = {}
        if code:
            token = sp_oauth.get_access_token(code)['access_token']
        if token:
            context_data = {
                'spotify_token': token
            }
            self.request.session['token'] = token
        return context_data


class PlaylistGenerateView(View):

    def get(self, request):
        lastfm_username = request.GET.get('lastfm_username')
        playlist_name = request.GET.get('playlist_name')
        spotify_token = (request.GET.get('spotify_token') or
                         request.session.get('token'))
        if not (lastfm_username and playlist_name and spotify_token):
            return JsonResponse(
                {'error': 'Bad request\nLastFM Username: {}\n'
                          'Playlist Name: {}\nSpotify token{}'
                          .format(lastfm_username, playlist_name, spotify_token)})
        playlist_tracks = get_playlist_tracks(lastfm_username)
        playlist_response = create_playlist(spotify_token, playlist_tracks)
        if 'error' in playlist_response:
            return JsonResponse(playlist_response, 500)
        return JsonResponse({'playlist': playlist_response})


class AuthSpotifyView(View):

    def get(self, request):
        sp_oauth = oauth2.SpotifyOAuth(SPOTIFY_API_KEY, SPOTIFY_API_SECRET, SPOTIFY_REDIRECT_URL,
                                       scope=SPOTIFY_SCOPES)
        auth_url = sp_oauth.get_authorize_url()
        return JsonResponse({'spotify_auth_url': auth_url})
