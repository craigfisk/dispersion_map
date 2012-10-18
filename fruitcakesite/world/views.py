from django.core.urlresolvers import reverse
from fruitcakesite.settings import MEDIA_ROOT, MEDIA_URL

def main(request):
    history = History.objects.all()
    return render_to_response('world/list.html', dict(history=history, user=request.user)
