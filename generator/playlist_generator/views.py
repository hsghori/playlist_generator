import json
from spotipy import oauth2, Spotify
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from .utils.playlist_creation import create_playlist


SPOTIFY_SCOPES = ' '.join([
    'user-top-read',
    'user-read-email',
    'playlist-read-private',
    'playlist-modify-private',
    'playlist-modify-public',
])


class LoginView(TemplateView):
    template_name = 'playlist_generator/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sp_oauth = oauth2.SpotifyOAuth(
            client_id=settings.SPOTIFY_API_KEY,
            client_secret=settings.SPOTIFY_API_SECRET,
            redirect_uri=settings.SPOTIFY_REDIRECT_URL,
            scope=SPOTIFY_SCOPES
        )
        context['spotify_auth_url'] = sp_oauth.get_authorize_url()
        return context


class AuthCallbackView(View):

    def get(self, request, *args, **kwargs):
        sp_oauth = oauth2.SpotifyOAuth(
            client_id=settings.SPOTIFY_API_KEY,
            client_secret=settings.SPOTIFY_API_SECRET,
            redirect_uri=settings.SPOTIFY_REDIRECT_URL,
            scope=SPOTIFY_SCOPES
        )
        code = self.request.GET.get('code')
        token = sp_oauth.get_access_token(code)['access_token']
        spotify = Spotify(auth=token)
        spotify_user = spotify.current_user()
        try:
            user = User.objects.get(username=spotify_user['id'])
        except User.DoesNotExist:
            user = User.objects.create(
                username=spotify_user['id'],
                password=spotify_user['id'],
                email=spotify_user['email'],
            )
        login(request, user)
        self.request.session['token'] = token
        return redirect('index')


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'playlist_generator/index.html'


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')


class PlaylistGenerateView(View):

    def post(self, request):
        params = json.loads(request.body)
        playlist_name = params.get('playlist_name')
        spotify_token = request.session.get('token')

        if not (playlist_name and spotify_token):
            error_message = 'Bad request\nPlaylist Name: %s\nSpotify token%s' % (
                playlist_name, spotify_token)
            return JsonResponse({'error': error_message}, status=400)

        playlist_response = create_playlist(spotify_token, playlist_name)
        if 'error' in playlist_response:
            return JsonResponse(playlist_response, 500)

        return JsonResponse({'playlist': playlist_response})
