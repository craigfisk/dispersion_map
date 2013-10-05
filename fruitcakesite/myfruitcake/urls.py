#from django.contrib.auth.decorators import login_required
#from django.views.generic import DetailView, ListView, TemplateView
from myfruitcake.models import Fruitcake, Shipment  # Upload
# MyFruitcakeListView, ShipmentListView, 
from myfruitcake.views import MyFruitcakeListView, ShipmentListView
#from myfruitcake.views import upload_file
#from myfruitcake.views import email_fruitcake
#from myfruitcake.views import about
#from myfruitcake.views import success 
#from myfruitcake.views import testmap
#from myfruitcake.views import search
#from myfruitcake.views import search_form
#from myfruitcake.views import meta
#from myfruitcake.views import path #activity 
#about_sample
#from fruitcakesite.views import FruitcakeListView
from django.conf.urls import patterns, url  #include
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('myfruitcake.views',
    url(r'^$', login_required(MyFruitcakeListView.as_view(model=Fruitcake)), name='myfruitcakelistview'),
    #url(r'^$', MyFruitcakeListView.as_view(model=Fruitcake), name='myfruitcakelistview',
    url(r'^myshipments', login_required(ShipmentListView.as_view(model=Shipment)), name='myshipments'),
    url(r'^upload/$', 'upload_file', name='myfruitcake_upload'),
    url(r'^about/$', 'about'),
#    url(r'^about_sample/$', 'about_sample'),
    url(r'^success/$', 'success'),
    url(r'(?P<fruitcake_id>\d+)/shipment/$', 'email_fruitcake'),
    url(r'^(?P<fruitcake_id>\d+)/shipment/(?P<shipment_id>\d+)/$', 'email_fruitcake'),
    url(r'^path/.*$', 'path'),
    url(r'^meta/.*$', 'meta'),
    url(r'^search-form/$', 'search_form'),
    url(r'^search/$', 'search'),
    url(r'^map/$', 'testmap'),
) 


