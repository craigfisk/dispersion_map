from string import join
from PIL import Image as PImage
from os.path import join as pjoin

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
#from django.utils.decorators import method_decorator

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from fruitcakesite.settings import MEDIA_ROOT, MEDIA_URL, WIDTH_AVATAR, WIDTH_FRUITCAKE

from myfruitcake.models import *
from forum.models import UserProfile
from forum.views import mk_paginator, UserProfile, profile

from django.views.generic import ListView, TemplateView, FormView

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
#        exclude = ["posts", "user"]

"""
@login_required
def main(request):
    return HttpResponseRedirect("/myfruitcake/")
#    fruitcake = Fruitcake.objects.all()
#    return render_to_response("myfruitcake/myfruitcake_list.html", dict(fruitcake=fruitcake, user=request.user))
"""

def activity(request, pk):
    #Listing of posts in a thread.
    shipments = Shipment.objects.all().order_by("dt")
    shipments = mk_paginator(request, shipments, 15)
    return render_to_response("myfruitcake/activity.html", add_csrf(request, shipments=shipments, media_url=MEDIA_URL))

class FruitcakeListView(ListView):
#    @method_decorator(login_required)
#    def dispatch(self, *args, **kwargs):
#        return super(FruitcakeListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FruitcakeListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        if self.request.user.id:
            return Fruitcake.objects.filter(uploader=self.request.user)
            # or: popup__startswith='Pick me'
        else:
            return Fruitcake.objects.all()
"""
class EmailTemplateView(FormView):
    template_name = 'email_fruitcake.html'
    def get_context_data(self, **kwargs):
        context = super(EmailTemplateView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def 
"""
from fruitcakesite.settings import DEFAULT_FROM_EMAIL
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django import forms

#EmailMultiAlternatives
    # For fields in class EmailMessage, see
    # https://docs.djangoproject.com/en/dev/topics/email/#django.core.mail.EmailMessage
#    subject = 'Fruitcake for you'
#    body = 'Fill in here'
#    from_email = DEFAULT_FROM_EMAIL 
#    to = 'wcraigfisk@gmail.com'
      
"""
class FruitcakeEmailForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_user = forms.BooleanField(required=True)
"""
class MyForm(forms.Form):
    pass

class FruitcakeEmailForm(forms.Form):
    class Meta:
        model = EmailMessage
        exclude = ["cc", "bcc", "body", "connection", "attachments", "headers"]

    def __init__(self, *args, **kwargs):
        super(FruitcakeEmailForm, self).__init__(*args, **kwargs)
#        self.fields['fruitcake_id'] = None 

    # keep: subject, to (list or tuple), from_email
    # https://docs.djangoproject.com/en/dev/topics/email/

from django.shortcuts import render

def email_fruitcake(request, pk, template_name='myfruitcake/email.html'):
#    fruitcake = get_object_or_404(Fruitcake, id=pk)
#    form = FruitcakeEmailForm(request.POST or None)
    form = MyForm(request.POST or None)
    if form.is_valid():
        form.fruitcake_id = pk
#        fruitcake.save()
        return redirect('myfruitcake/success.html')
    return render(request, template_name, {'form':form}) 


"""
def email_fruitcake(request, pk):
    # pk ?
    if request.method == "POST":
        form = FruitcakeEmailForm(request.POST)

        if form.is_valid():
           form.send()
            return HttpResponseRedirect('/myfruitcake/')

    else:
        form = FruitcakeEmailForm()

#    return render(request, 'myfruitcake/email.html', add_csrf(request, form=form)) 
    return render_to_response('myfruitcake/email.html', add_csrf(request, form=form)) 
    #return render_to_response('myfruitcake/email.html', add_csrf(request, form=form))

#    return HttpResponse("Got this far -- fruitcake id: %s, request.user: %s, request.user.email: %s, DEFAULT_FROM_EMAIL:  %s, fruitcake_url: %s" % (pk, request.user, request.user.email, DEFAULT_FROM_EMAIL, fruitcake_url))
"""

"""
class MyFruitcakeListView(ListView):
    template_name = 'myfruitcake_list.html'
    context_object_name = 'myfruitcake_list'
    def get_context_data(self, **kwargs):
        context = super(MyFruitcakeListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        return Fruitcake.objects.filter(user=self.request.user)
"""


from django import forms

from django.db import models
from django.forms import ModelForm

class UploadFruitcakeForm(ModelForm):
    class Meta:
        model = Fruitcake
        exclude = ['uploader', 'shipments', 'uploads', 'source', 'thumbnail']

class LikeForm(ModelForm):
    class Meta:
        model = Like
        exclude = ['dt', 'fruitcake', 'user'] 

@login_required
def upload_file(request):

    if request.method == "POST":

        form = UploadFruitcakeForm(request.POST, request.FILES)
        if form.is_valid():
            pic = form.save(commit=False)
            # resize is a now customization of save() in the class
            # then add the request.user
            pic.uploader = request.user
            pic.save()
            #form.save()
#            return HttpResponseRedirect('/myfruitcake/success/')
            return HttpResponseRedirect('/myfruitcake/')

    else:
        form = UploadFruitcakeForm()

    return render_to_response('myfruitcake/upload.html', add_csrf(request, form=form)) 

def success(request):
    return HttpResponse("Success!")

def add_csrf(request, **kwargs):
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d

#-------------------------------
from django.http import HttpResponse

@staff_member_required
def path(request):
    s = "Hello world<br />"
    s+= " request.path: %s<br />" % (request.path)
    s+= " request.get_full_path(): %s<br />" % (request.get_full_path() )
    s+= " request.get_host(): %s<br />" % (request.get_host() )
    s+= " request.is_secure(): %s<br />" % (request.is_secure() )
    return HttpResponse(s)

@staff_member_required
def meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k,v in values:
        html.append('<tr><td>%s</td></tr><tr><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

from django.shortcuts import render_to_response
#from myfruitcake.models import Fruitcake

@staff_member_required
def search_form(request):
    return render_to_response('myfruitcake/search_form.html', {'user': request.user} )

@staff_member_required
def search(request):
    profile = UserProfile.objects.get(user=request.user)
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Please enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            fruitcakes = Fruitcake.objects.filter(popup__icontains=q)
            if len(fruitcakes):
                return render_to_response('myfruitcake/search_results.html', {'fruitcakes': fruitcakes, 'query':q,
                    'user':request.user})
            else:
                errors.append('No results for that search.')

    return render_to_response('myfruitcake/search_form.html', {'errors': errors, 'user': request.user} )


