from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fruitcakesite.views.home', name='home'),
    # url(r'^fruitcakesite/', include('fruitcakesite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^voting/$', 'voting.views.index'),
    url(r'^voting/(?P<poll_id>\d+)/$', 'voting.views.detail'),
    url(r'^voting/(?P<poll_id>\d+)/results/$', 'voting.views.results'),
    url(r'^voting/(?P<poll_id>\d+)/vote/$', 'voting.views.vote'),

)
