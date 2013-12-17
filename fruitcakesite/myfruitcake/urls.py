from myfruitcake.models import Fruitcake, Shipment 
from myfruitcake.views import MyFruitcakeListView, MyFruitcakeDetailView, ShipmentListView, ShipmentDetailView, FruitcakeListView, termsofservice
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from lazysignup.decorators import allow_lazy_user   # replaces login_required() below and in myfruitcake.views

urlpatterns = patterns('myfruitcake.views',
    url(r'^$', FruitcakeListView.as_view(), name='toplistview'),
    url(r'^myfruitcake/$', allow_lazy_user(MyFruitcakeListView.as_view()), name='listview'),                         #all lr -> alu
    url(r'^myfruitcake/(?P<pk>\d+)/$', allow_lazy_user(MyFruitcakeDetailView.as_view()), name='detailview'),         #one +alu
    url(r'^myfruitcake/(?P<fruitcake_id>\d+)/send/$', 'email_fruitcake', name='send_fruitcake'),                      #send [see views.py]

    url(r'^myshipments/$', allow_lazy_user(ShipmentListView.as_view()), name='shipments'),                           #all lr -> alu
    url(r'^myshipments/(?P<pk>\d+)/$', allow_lazy_user(ShipmentDetailView.as_view()), name='shipment_detail'),       #one +alu
    url(r'^myshipments/(?P<shipment_id>\d+)/send/$', 'email_fruitcake', name='send_fruitcake'),                       #send [see views.py]
    
   
    url(r'^upload/$', 'upload_file', name='myfruitcake_upload'),
    url(r'^about/$', 'about', name='about'),
    url(r'^termsofservice/$', 'termsofservice', name='termsofservice'),
#    url(r'^success/$', 'success', name='myfruitcake_success'),

    url(r'^path/.*$', 'path', name='path'),
    url(r'^meta/.*$', 'meta', name='meta'),
#    url(r'^search-form/$', 'search_form', name='myfruitcake_search_form'),
    url(r'^search/$', 'search', name='search'),
    #url(r'^map/$', 'testmap', name='testmap'),
#    url(r'^duplicate/$', 'duplicate', name='myfruitcake_duplicate'),
) 


