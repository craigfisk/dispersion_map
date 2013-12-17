from django.conf.urls import patterns, include, url
from myfruitcake.models import Fruitcake, Shipment
from forum.models import UserProfile, Forum, Thread, Post
from django.contrib import admin
from fruitcakesite.views import index
#from django.http import HttpResponse

import warnings
warnings.simplefilter('error', DeprecationWarning)

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'admin/', include(admin.site.urls)),
    url(r'forum/', include('forum.urls', namespace='forum')),
    #url(r'forum/', HttpResponse("Coming soon!")),

    url(r'myfruitcake/', include('myfruitcake.urls', namespace='fruitcake')),
    url(r'^registration/login/$', 'fruitcakesite.views.login'),
    url(r'^registration/', include('registration.backends.default.urls')),
    url(r'^convert/', include('lazysignup.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'} )
)

