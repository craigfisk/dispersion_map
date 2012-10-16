from django.conf.urls import patterns, include, url
from fruitcakesite.views import main_page

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', main_page),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include('polls.urls')),
    url(r'^myaccount/', include('myaccount.urls')),
)
