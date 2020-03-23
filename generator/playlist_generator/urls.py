from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^auth_callback/$', views.AuthCallbackView.as_view(), name='auth_callback'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),
    url(r'^create_playlist/$', views.PlaylistGenerateView.as_view(),
        name="create-playlist"),
]
