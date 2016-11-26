from django.views.generic.base import TemplateView
from django.http import JsonResponse, HttpResponse
from core import utils
from django.template.loader import render_to_string


class VideoPlayerView(TemplateView):
    template_name = 'videostream/videoplayer.html'


class VideoFileExplorer(TemplateView):
    template_name = 'videostream/videofileexplorer.html'

    def get_context_data(self, **kwargs):
        return {'tree': utils.getFileTree()}


def FileExplorerChildren(request):
    prefix = request.POST['url_prefix']
    print('POST DATA', prefix)

    html = render_to_string('videostream/explorersection.html', {'tree': utils.getFileTree(root=prefix)})
    return HttpResponse(html)
    # return JsonResponse(utils.getFileTree(root=prefix))
