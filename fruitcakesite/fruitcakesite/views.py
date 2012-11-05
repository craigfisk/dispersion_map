from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
#from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def home_page(request):
#    return render_to_response('index.html')
#    if not request.user.is_authenticated():
     return render_to_response('index.html', context_instance=RequestContext(request))
#    render_to_response('forum.html', context_instance=RequestContext(request))
   
def logout_page(request):
    """
    Log user out and redirect to main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

