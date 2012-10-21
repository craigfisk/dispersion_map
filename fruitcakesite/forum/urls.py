from django.conf.urls.defaults import *
from forum.models import *
from forum.views import *
#main, forum, thread, post, reply, profile, new_thread, add_csrf

urlpatterns = patterns('forum.views',
    (r'^forum/(\d+)/$', 'forum'),
    (r"^thread/(\d+)/$", "thread"),
    (r"^post/(new_thread|reply)/(\d+)/$", "post"),
    (r"^reply/(\d+)/$", "reply"),
    (r"^profile/(\d+)/$", "profile"),
#    (r"^save_profile/(\d+)/$", "save_profile"),
    (r"^new_thread/(\d+)/$", "new_thread"),
    (r"", "main"),
)
