from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, TemplateView
from myfruitcake.models import Fruitcake, Upload, Shipment
from myfruitcake.views import activity, upload_file, MyFruitcakeListView, ShipmentListView, email_fruitcake, about
#about_sample
from fruitcakesite.views import FruitcakeListView
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('myfruitcake.views',
    url(r'^$', login_required(MyFruitcakeListView.as_view(model=Fruitcake)), name='myfruitcakelistview'),
    #url(r'^$', MyFruitcakeListView.as_view(model=Fruitcake), name='myfruitcakelistview',
    url(r'^myshipments', login_required(ShipmentListView.as_view(model=Shipment)), name='myshipments'),
    url(r'^upload/$', 'upload_file'),
    url(r'^about/$', 'about'),
#    url(r'^about_sample/$', 'about_sample'),
    url(r'^success/$', 'success'),
    url(r'(?P<fruitcake_id>\d+)/shipment/$', 'email_fruitcake'),
    url(r'^(?P<fruitcake_id>\d+)/shipment/(?P<shipment_id>\d+)/$', 'email_fruitcake'),
    url(r'^path/.*$', 'path'),
    url(r'^meta/.*$', 'meta'),
    url(r'^search-form/$', 'search_form'),
    url(r'^search/$', 'search'),
) 


