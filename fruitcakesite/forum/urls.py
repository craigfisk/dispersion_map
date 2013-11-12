#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url
#from forum.models import UserProfile, Thread, Post, Forum
#from forum.views import main, forum, thread, post, reply, profilepic, userinfo, new_thread
#main, forum, thread, post, reply, profile, new_thread, add_csrf


urlpatterns = patterns('forum.views',
    url(r'^forum/(\d+)/$', 'forum', name='forum_content'),
    url(r'^thread/(\d+)/$', 'thread', name='forum_thread'),
    url(r'^post/(new_thread|reply)/(\d+)/$', 'post', name='forum_post'),
    url(r'^reply/(\d+)/$', 'reply', name='forum_reply'),
    #url(r'^profilepic/(\d+)$', 'profilepic', name='forum_profilepic'),
    url(r'^profilepic/$', 'profilepic', name='forum_profilepic'),
    #url(r'^userinfo/(\d+)$', 'userinfo', name='forum_userinfo'),
    url(r'^userinfo/$', 'userinfo', name='forum_userinfo'),
    url(r'^new_thread/(\d+)/$', 'new_thread', name='forum_new_thread'),
    url(r'', 'main', name="forum_main"),
)
