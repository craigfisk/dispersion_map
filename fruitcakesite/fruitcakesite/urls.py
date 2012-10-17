from django.conf.urls import patterns, include, url
from fruitcakesite.views import main_page, logout_page

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', main_page),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include('polls.urls')),
    url(r'^myaccount/', include('myaccount.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'} ),
)
