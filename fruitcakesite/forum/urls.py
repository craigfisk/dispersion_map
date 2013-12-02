from django.conf.urls import patterns, url

urlpatterns = patterns('forum.views',
    url(r'^forum/$', 'main', name='forum_main'),
    url(r'^forum/(\d+)/$', 'forum', name='forum_content'),
    url(r'^thread/(\d+)/$', 'thread', name='forum_thread'),
    url(r'^post/(new_thread|reply)/(\d+)/$', 'post', name='forum_post'),
    url(r'^reply/(\d+)/$', 'reply', name='forum_reply'),
    url(r'^profilepic/$', 'profilepic', name='profilepic'),
    url(r'^userinfo/$', 'userinfo', name='userinfo'),
    url(r'^new_thread/(\d+)/$', 'new_thread', name='forum_new_thread'),
)
