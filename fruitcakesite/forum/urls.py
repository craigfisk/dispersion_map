#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include
from forum.models import UserProfile, Thread, Post, Forum
from forum.views import main, forum, thread, post, reply, profilepic, userinfo, new_thread
#main, forum, thread, post, reply, profile, new_thread, add_csrf


urlpatterns = patterns('forum.views',
    url(r'^forum/(\d+)/$', 'forum'),
    url(r'^thread/(\d+)/$', 'thread'),
    url(r'^post/(new_thread|reply)/(\d+)/$', 'post'),
    url(r'^reply/(\d+)/$', 'reply'),
    url(r'^profilepic/(\d+)/$', 'profilepic'),
    url(r'^userinfo/(\d+)/$', 'userinfo'),
    url(r'^new_thread/(\d+)/$', 'new_thread'),
    url(r'', 'main'),
)
