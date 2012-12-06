from django.conf.urls import patterns, include, url
from myfruitcake.models import Fruitcake, Shipment
from forum.models import UserProfile, Forum, Thread, Post
from fruitcakesite.views import home_page, logout_page
from django.contrib import admin
from myfruitcake.views import FruitcakeListView
admin.autodiscover()

urlpatterns = patterns('',
##    url(r'^$', home_page),
    url(r'^$', FruitcakeListView.as_view(model=Fruitcake), name='home'),
#    url(r'^home/$', home),
##    url(r'^$', main),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
    url(r'^admin/', include(admin.site.urls)),
#    url(r'^polls/', include('polls.urls')),
    url(r'forum/', include('forum.urls')),
    url(r'myfruitcake/', include('myfruitcake.urls')),
##    url(r'^world/', include('world.urls')),
    # CF20121104 changed next line from 'registration.urls' (deprecated) to 'registration.backends.default.urls'?
    # See http://docs.b-list.org/django-registration/0.8/upgrade.html on how to rewrite for changes to the API
    # accounts -> registration. Update CF20121205: not clear what "deprecated" means here, because a customization
    # of the site-packages/registration urlconf would be at fruitcakesite/registration/urls.py, which would be
    # include('registration.urls').
    # url(r'^registration/', include('registration.urls')),
    url(r'^registration/', include('registration.backends.default.urls')),
    #
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'} ),
)

# django-registration latest (see above):
# - How to upgrade for latest (0.8):  http://docs.b-list.org/django-registration/0.8/upgrade.html
# - Template examples from Matias Herranz at https://github.com/matiasherranz/scoobygalletas/downloads
# - Tutorial:  see "Django by Example" part 3, http://lightbird.net/dbe/forum3.html (helpful but deprecated
# registration.urls etc. model)

