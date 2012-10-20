from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from accounts.models import UserProfile
from accounts.views import accounts_home

urlpatterns = patterns('', 
    url(r'^$', accounts_home),
)



