from django.conf.urls import url
from videostream import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'videostream'

urlpatterns = [
    url(r'^play/$', views.VideoPlayerView.as_view(), name='video-player'),
    url(r'^videos/$', views.VideoFileExplorer.as_view(), name='video-file-explorer'),
    url(r'^getChildren/$', views.FileExplorerChildren, name='video-get-children'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

