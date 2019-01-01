from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from playlist_generator.views import IndexView, PlaylistGenerateView, AuthSpotifyView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^create_playlist/$', PlaylistGenerateView.as_view(),
        name="create-playlist"),
    url(r'^auth_spotify/$', AuthSpotifyView.as_view(), name='get_spotify_url')
]

urlpatterns += staticfiles_urlpatterns()
