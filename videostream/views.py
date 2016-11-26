from django.views.generic.base import TemplateView
from django.http import JsonResponse
from core import utils


class VideoPlayerView(TemplateView):
    template_name = 'videostream/videoplayer.html'


class VideoFileExplorer(TemplateView):
    template_name = 'videostream/videofileexplorer.html'

    def get_context_data(self, **kwargs):
        return {'tree': utils.getFileTree()}


# def FileExplorerChildren():
#
#     return JsonResponse(utils.getChildren())
