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

from django.views.generic import ListView

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
#        exclude = ["posts", "user"]

"""
def main(request):
    #Main listing for myfruitcake.
    fruitcake = Fruitcake.objects.all()
    return render_to_response("myfruitcake/list.html", dict(fruitcake=fruitcake, user=request.user))
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
        return Fruitcake.objects.filter(uploader=self.request.user)
        # or: popup__startswith='Pick me'

class MyFruitcakeListView(ListView):
    template_name = 'myfruitcake_list.html'
    context_object_name = 'myfruitcake_list'
    def get_context_data(self, **kwargs):
        context = super(MyFruitcakeListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        return Fruitcake.objects.filter(user=self.request.user)



from django import forms

#class UploadImageFileForm(forms.Form):
#    title = forms.CharField(max_length=50)
#    file = forms.FileField()

from django.db import models
from django.forms import ModelForm

class UploadFruitcakeForm(ModelForm):
    class Meta:
        model = Fruitcake
        exclude = ['uploader', 'shipments', 'uploads', 'source', 'thumbnail']
"""
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFruitcakeForm(request.POST, request.FILES)
        if form.is_valid():
            # do something to
            # handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/')
    else:
        form = UploadFruitcakeForm()
#    return render_to_response('myfruitcake/upload.html', {'form': form})
    return render_to_response('myfruitcake/upload.html', add_csrf(request, form=form))
"""

#def make_fruitcake(request, pk):

@login_required
def upload_file(request):
##    profile = UserProfile.objects.get(user=pk)

    if request.method == "POST":
##        pf = ProfileForm(request.POST, request.FILES, instance=profile)
       
#        im = PImage.open(pjoin(MEDIA_ROOT, request.FILES['pic'])
#        imfn = pjoin(MEDIA_ROOT, request.FILES['pic'])

        form = UploadFruitcakeForm(request.POST, request.FILES)
        if form.is_valid():
            pic = form.save(commit=False)
            # resize it first
            #request.FILES['pic'])
            """)
            try:
                im = PImage.open(imfn)
                # 160, 160 --> 120,120 CF20121023:
                ##im.thumbnail((120, 120), PImage.ANTIALIAS)
                wpercent = (WIDTH_FRUITCAKE/float(im.size[0]))
                hsize = int((float(im.size[1])*float(wpercent)))
                im = im.resize((WIDTH_FRUITCAKE, hsize), PImage.ANTIALIAS)
                im.save(imfn, "JPEG")
            except IOError:
                print "Cannot resize ", imfn
            """
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

#        pf = ProfileForm(instance=profile)

##    if profile.avatar:
##        img = MEDIA_URL + profile.avatar.name
##    return render_to_response("forum/profile.html", add_csrf(request, pf=pf, img=img))

def add_csrf(request, **kwargs):
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d

