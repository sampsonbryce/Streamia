from django.views.generic.base import TemplateView


class VideoPlayerView(TemplateView):
    template_name = 'videostream/videoplayer.html'
