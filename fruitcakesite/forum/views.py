import logging
logger = logging.getLogger(__name__)
from fruitcakesite.settings import FUNCTION_LOGGING

#from string import join
from PIL import Image as PImage
from os.path import join as pjoin

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect #, HttpResponse
from django.shortcuts import render_to_response #get_object_or_404, 
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from fruitcakesite.settings import MEDIA_ROOT, MEDIA_URL, WIDTH_AVATAR
from django.template import RequestContext
from django import forms
from forum.models import Forum, Thread, Post, UserProfile
from django.db import models

#CF20131021 hmm, looks like this is superceded by class UserProfile (avatar, user, posts, shipments) in forum.models
"""
class UserProfile(models.Model):
    # was upload_to="images/" in Django by Example but ReadTheDocs "How do I use image and file fields" says MEDIA_ROOT
    # See http://readthedocs.org/docs/django/en/latest/faq/usage.html#how-do-i-use-image-and-file-fields
    # Also in forum/models.py
    avatar = models.ImageField("Profile Pic", upload_to='images', blank=True, null=True)
    posts = models.IntegerField(default=0)
    user = models.ForeignKey(User, unique=True)

    def __unicode__(self):
        return unicode(self.user)
"""

class ProfileForm(ModelForm):
    class Meta:
        if FUNCTION_LOGGING:  logger.debug("Entering class ProfileForm")
        model = UserProfile
        exclude = ["user", "posts", "shipments"]

class UserForm(ModelForm):
    class Meta:
        if FUNCTION_LOGGING:  logger.debug("Entering class UserForm")
        model = User
        exclude = ["first_name","last_name","password","is_staff","is_active","is_superuser","last_login","date_joined","groups","user_permissions"]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        #self.fields['username'].widget = forms.TextInput(attrs={'size':'32'}) 
        self.fields['email'].widget = forms.TextInput(attrs={'size':'32'}) 

def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items

@login_required
def main(request):
    forums = Forum.objects.all()
    return render_to_response("forum/contents.html", dict(forums=forums, user=request.user), context_instance=RequestContext(request))

@login_required
def forum(request, pk):
    """Listing of threads in a forum."""
    threads = Thread.objects.filter(forum=pk).order_by("-created")
    threads = mk_paginator(request, threads, 20)
    #CF20121111 added the bits here with title, on the model of what is done in thread(). Also added title=title in
    # the render_to_response.
    title = Forum.objects.get(pk=pk) 
    return render_to_response("forum/forum.html", add_csrf(request, threads=threads, pk=pk, title=title), context_instance=RequestContext(request))

@login_required
def thread(request, pk):
    """Listing of posts in a thread."""
    posts = Post.objects.filter(thread=pk).order_by("created")
    posts = mk_paginator(request, posts, 15)
    #title = Thread.objects.get(pk=pk).title
    t = Thread.objects.get(pk=pk)
    return render_to_response("forum/thread.html", add_csrf(request, posts=posts, pk=pk, title=t.title,
        forum_pk=t.forum.pk, media_url=MEDIA_URL), context_instance=RequestContext(request))
    # forum_pk=t.forum.pk


@login_required
def profilepic(request, pk):
    if FUNCTION_LOGGING:  logger.debug("Entering profilepic()")

    profile = UserProfile.objects.get(user=pk)
    img = None

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        #form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # resize and save image under same filename
            ##imfn = pjoin(MEDIA_ROOT, request.FILES['avatar'])
            imfn = pjoin(MEDIA_ROOT, profile.avatar.name)
            #imfn = pjoin(MEDIA_ROOT, profile.avatar.name)
            #CF20121023 adding try/except framework, per PIL-handbook p. 3
            """
            im = PImage.open(imfn)
            # 160, 160 --> 120,120 CF20121023:
            im.thumbnail((120,120), PImage.ANTIALIAS)
            im.save(imfn, "JPEG")
            """
            try:
                im = PImage.open(imfn)
                # 160, 160 --> 120,120 CF20121023:
                ##im.thumbnail((120,120), PImage.ANTIALIAS)
                wpercent = (WIDTH_AVATAR/float(im.size[0]))
                hsize = int((float(im.size[1])*float(wpercent)))
                im = im.resize((WIDTH_AVATAR, hsize), PImage.ANTIALIAS)
                im.save(imfn, "JPEG")
            except IOError as e:
                print "Cannot create thumbnail for %s, error: %s" % (imfn, e)
            
    else:
        form = ProfileForm(instance=profile)
        #form = ProfileForm()
    if profile.avatar:
        img = MEDIA_URL + profile.avatar.name
    #uf = UserForm(request.POST, instance=profile.user)
    return render_to_response("forum/profilepic.html", add_csrf(request, profile=profile, form=form, img=img), context_instance=RequestContext(request))
    #return render_to_response("forum/userinfo.html", add_csrf(request, uf=uf, u=profile.user, img=img), context_instance=RequestContext(request))
    #return HttpResponseRedirect(reverse("forum.views.userinfo", args=[pk]))


@login_required
def userinfo(request, pk):
    if FUNCTION_LOGGING:  logger.debug("Entering userinfo()")
    u = User.objects.get(pk=pk)

    if request.method == "POST":
        uf = UserForm(request.POST, instance=u)
        if uf.is_valid():
            uf.save()
           
    else:
        uf = UserForm(instance=u)

    #if u.userprofile.avatar.name:
    #    img = MEDIA_URL + u.userprofile.avatar.name
    return render_to_response("forum/userinfo.html", add_csrf(request, uf=uf, u=u), context_instance=RequestContext(request))



@login_required
def post(request, ptype, pk):
    if FUNCTION_LOGGING:  logger.debug("Entering post()")
  
    action = reverse("forum.views.%s" % ptype, args=[pk])
    if ptype == "new_thread":
        title = "Start New Topic"
        subject = ''
    elif ptype == "reply":
        title = "Reply"
        subject = "Re: " + Thread.objects.get(pk=pk).title

    return render_to_response("forum/post.html", add_csrf(request, subject=subject, action=action, title=title), context_instance=RequestContext(request))

def increment_post_counter(request):
    #CF20121105 changed to match user.userprofile structure
#    profile = request.user.userprofile_set.all()[0]
    profile = request.user.userprofile
    profile.posts += 1
    profile.save()

@login_required
def new_thread(request, pk):
    if FUNCTION_LOGGING:  logger.debug("Entering new_thread()")
 
    p = request.POST
    if p["subject"] and p["body"]:
        forum = Forum.objects.get(pk=pk)
        thread = Thread.objects.create(forum=forum, title=p["subject"], creator=request.user)
        Post.objects.create(thread=thread, title=p["subject"], body=p["body"], creator=request.user)
        increment_post_counter(request)
    return HttpResponseRedirect(reverse("forum.views.forum", args=[pk]))

@login_required
def reply(request, pk):
    if FUNCTION_LOGGING:  logger.debug("Entering reply()")
 
    p = request.POST
    if p["body"]:
        thread = Thread.objects.get(pk=pk)
        post = Post.objects.create(thread=thread, title=p["subject"], body=p["body"], creator=request.user)
        increment_post_counter(request)
    return HttpResponseRedirect(reverse("forum.views.thread", args=[pk]) + "?page=last")

def add_csrf(request, **kwargs):
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d

