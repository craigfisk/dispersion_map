from django.http import HttpResponseRedirect

from django.conf import settings

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/myfruitcake/')
    else:
        return HttpResponseRedirect('/myfruitcake/myshipments/')


