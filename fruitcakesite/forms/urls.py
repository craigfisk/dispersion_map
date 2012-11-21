from django.http import HttpResponse
from django.conf.urls import patterns, include, url

from forms.views import path, meta, search_form, search

urlpatterns = patterns('forms.views',
#    url(r"", "main"),
    url(r'^path/.*$', 'path'),
    url(r'^meta/.*$', 'meta'),
    url(r'^search-form/$', 'search_form'),
    url(r'^search/$', 'search'),
    #    url(r'^email/(\d+)/$', 'email_fruitcake'),
)
