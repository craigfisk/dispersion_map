from string import join
from PIL import Image as PImage
from os.path import join as pjoin

#CF20121107 todo: probably can cut some of these ...
from django.contrib.auth.decorators import login_required
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
from forum.views import mk_paginator

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

class FruitcakeEmailForm(forms.Form):
    class Meta:
        model = EmailMessage 
    fc = forms.CharField(widget=forms.HiddenInput)

from django.shortcuts import render

def email_fruitcake(request, fc=0):
    if fc: 
        fruitcake = Fruitcake.objects.get(id=fc)
    if request.method == "POST":
        form = FruitcakeEmailForm(request.POST)
        form.subject = "Fruitcake for you: %s" % (request.POST['fc'])
        form.body = 'Happy holidays!'
        form.from_email = DEFAULT_FROM_EMAIL
        form.to = request.POST['to'] 
        form.cc = request.user.email
        if form.is_valid():
            email = EmailMessage(form.subject, form.body, form.from_email, form.to)
            email.send(fail_silently=False)
            return HttpResponseRedirect('/myfruitcake/')
        else:
            return HttpResponse("There was a problem. %s, %s, %s" % (form.subject, form.from_email, form.to))
    else:
        form = FruitcakeEmailForm()
    return render_to_response('myfruitcake/email.html', add_csrf(request, form=form)) 


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

