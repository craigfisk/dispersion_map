from django.http import HttpResponse

def path(request):
    s = "Hello world<br />"
    s+= " request.path: %s<br />" % (request.path)
    s+= " request.get_full_path(): %s<br />" % (request.get_full_path() )
    s+= " request.get_host(): %s<br />" % (request.get_host() )
    s+= " request.is_secure(): %s<br />" % (request.is_secure() )
    return HttpResponse(s)

def meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k,v in values:
        html.append('<tr><td>%s</td></tr><tr><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

from django.shortcuts import render_to_response
from myfruitcake.models import Fruitcake

def search_form(request):
    return render_to_response('forms/search_form.html')

def search(request):
    if 'q' in request.GET and request.GET['q']:
        message = 'You searched for: %r<br />' % request.GET['q']
        """
        q = request.GET['q']
        fruitcakes = Fruitcake.objects.filter(popup__icontains=q)
        if fruitcakes:
            return render_to_response('forms/search_results.html', {'fruitcakes': fruitcakes, 'query':q})
        else:
            message += 'No fruitcake for you.'
        """
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)


