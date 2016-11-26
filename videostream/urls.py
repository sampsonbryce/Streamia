from django.conf.urls import url
from videostream import views

app_name = 'videostream'

urlpatterns = [
    url(r'^play/$', views.VideoPlayerView.as_view(), name='video-player'),
    url(r'^videos/$', views.VideoFileExplorer.as_view(), name='video-file-explorer'),
]
