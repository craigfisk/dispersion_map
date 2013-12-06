from django.conf.urls import patterns, url

urlpatterns = patterns('forum.views',
    url(r'^forum/$', 'main', name='forum_main'),
    url(r'^forum/(\d+)/$', 'forum', name='forum_content'),
    url(r'^thread/(\d+)/$', 'thread', name='forum_thread'),

    #url(r'^new_thread/(\d+)/$', 'new_thread', name='forum_new_thread'),
    #url(r'^reply/(\d+)/$', 'reply', name='forum_reply'),

    url(r'^combo/(?P<ptype>\w+)/(?P<post_id>\d+)/$', 'combo', name='combo'),
    #url(r'^post/(new_thread|reply)/(\d+)/$', 'post', name='forum_post'),
    url(r'^add_thread/(\d+)/$', 'add_thread', name='forum_add_thread'),
    url(r'^add_post/(\d+)/$', 'add_post', name='forum_add_post'),

    url(r'^profilepic/$', 'profilepic', name='profilepic'),
    url(r'^userinfo/$', 'userinfo', name='userinfo'),
)
