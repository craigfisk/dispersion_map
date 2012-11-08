from string import join
from PIL import Image as PImage
from os.path import join as pjoin

#CF20121107 todo: probably can cut some of these ...
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from fruitcakesite.settings import MEDIA_ROOT, MEDIA_URL, WIDTH_AVATAR

from myfruitcake.models import *

from django.views.generic import ListView

"""
def main(request):
    #Main listing for myfruitcake.
    fruitcake = Fruitcake.objects.all()
    return render_to_response("myfruitcake/list.html", dict(fruitcake=fruitcake, user=request.user))
"""

def activity(request, pk):
    """Listing of posts in a thread."""
    shipments = Shipment.objects.all().order_by("dt")
    shipments = mk_paginator(request, shipments, 15)
    return render_to_response("myfruitcake/activity.html", add_csrf(request, shipments=shipments, media_url=MEDIA_URL))

class FruitcakeListView(ListView):
    def get_context_data(self, **kwargs):
        context = super(FruitcakeListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Fruitcake.objects.all()

from django import forms

class UploadImageFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

def upload_file(request):
    if request.method == 'POST':
        form = UploadImageFileForm(request.POST, request.FILES)
        if form.is_valid():
            # do something to
            # handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/')
    else:
        form = UploadImageFileForm()
    return render_to_response('upload.html', {'form': form})

    return render_to_response('Nothing to see yet')

"""
def make_fruitcake(request, pk):
    profile = UserProfile.objects.get(user=pk)
    img = None

    if request.method == "POST":
        pf = ProfileForm(request.POST, request.FILES, instance=profile)
        if pf.is_valid():
            pf.save()
            # resize and save image under same filename
            imfn = pjoin(MEDIA_ROOT, profile.avatar.name)
            #CF20121023 adding try/except framework, per PIL-handbook p. 3
            try:
                im = PImage.open(imfn)
                # 160, 160 --> 120,120 CF20121023:
                ##im.thumbnail((120, 120), PImage.ANTIALIAS)
                wpercent = (WIDTH_AVATAR/float(im.size[0]))
                hsize = int((float(im.size[1])*float(wpercent)))
                im = im.resize((WIDTH_AVATAR, hsize), PImage.ANTIALIAS)
                im.save(imfn, "JPEG")
            except IOError:
                print "Cannot create thumbnail for ", imfn
            
    else:
        pf = ProfileForm(instance=profile)

    if profile.avatar:
        img = MEDIA_URL + profile.avatar.name
    return render_to_response("forum/profile.html", add_csrf(request, pf=pf, img=img))
# remove '/' from front of /media/ in "img" line above ??

"""

