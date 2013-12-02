from django.conf.urls import patterns, include, url
from myfruitcake.models import Fruitcake, Shipment
from forum.models import UserProfile, Forum, Thread, Post
#from myfruitcake.views import email_fruitcake
from django.contrib import admin

from fruitcakesite.views import FruitcakeListView

import warnings
warnings.simplefilter('error', DeprecationWarning)

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'forum/', include('forum.urls')),
    url(r'myfruitcake/', include('myfruitcake.urls')),
    url(r'^$', FruitcakeListView.as_view(model=Fruitcake), name='fruitcakelistview'),
    #url(r'^(?P<fruitcake_id>\d+)/shipment/$', 'myfruitcake.views.email_fruitcake'),
    url(r'^registration/', include('registration.backends.default.urls')),
    #url(r'^registration/login/', include('registration.backends.default.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'} )
)

