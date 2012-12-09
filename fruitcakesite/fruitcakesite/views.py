from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
#from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from myfruitcake.models import Fruitcake
from django.views.generic import ListView


class FruitcakeListView(ListView):
#    @method_decorator(login_required)
#    def dispatch(self, *args, **kwargs):
#        return super(FruitcakeListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FruitcakeListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        return Fruitcake.objects.all().order_by('-dt')[:16]



def home_page(request):
    return render_to_response('myfruitcake/fruitcake_list.html', context_instance=RequestContext(request))
#   return render_to_response('index.html', context_instance=RequestContext(request))
    """
    if not request.user.is_authenticated():
        return render_to_response('index.html', context_instance=RequestContext(request))
    else:
#        return HttpResponseRedirect('/myfruitcake/')
        return render_to_response('myfruitcake/fruitcake_list.html', context_instance=RequestContext(request))

#    render_to_response('forum.html', context_instance=RequestContext(request))
   """

def logout_page(request):
    """
    Log user out and redirect to main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

