from django.http import HttpResponseRedirect

from django.conf import settings

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/myfruitcake/')
    else:
        return HttpResponseRedirect('/myfruitcake/myshipments/')

# See https://djangosnippets.org/snippets/1881/
# and http://avivgr.blogspot.com/2009/05/how-to-add-remember-me-checkbox-to.html

from django.contrib.auth import views as auth_views
from fruitcakesite.settings import SESSION_COOKIE_AGE

def login(request, *args, **kwargs):
    if request.method == 'POST':
        # if checked, set to settings SESSION_COOKIE_AGE; else to 0 
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(SESSION_COOKIE_AGE)
    return auth_views.login(request, *args, **kwargs)

