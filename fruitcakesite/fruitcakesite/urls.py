from django.conf.urls import patterns, include, url
from myfruitcake.models import Fruitcake, Shipment
from forum.models import UserProfile, Forum, Thread, Post
from django.contrib import admin

import warnings
warnings.simplefilter('error', DeprecationWarning)

admin.autodiscover()

urlpatterns = patterns('',
    url(r'admin/', include(admin.site.urls)),
    url(r'forum/', include('forum.urls')),
    url(r'myfruitcake/', include('myfruitcake.urls')),
    url(r'^registration/', include('registration.backends.default.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'} )
)

