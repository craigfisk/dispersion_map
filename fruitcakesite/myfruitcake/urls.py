from myfruitcake.models import Fruitcake, Shipment 
from myfruitcake.views import MyFruitcakeListView, MyFruitcakeDetailView, ShipmentListView, ShipmentDetailView, FruitcakeListView
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('myfruitcake.views',

    url(r'^$', FruitcakeListView.as_view(), name='toplistview'),
    
    url(r'^myfruitcake/$', login_required(MyFruitcakeListView.as_view()), name='listview'),         #all
    url(r'^myfruitcake/(?P<pk>\d+)/$', MyFruitcakeDetailView.as_view(), name='detailview'),         #one
    url(r'^myfruitcake/(?P<fruitcake_id>\d+)/send/$', login_required('email_fruitcake'), name='send_fruitcake'),    #send

    url(r'^myshipments/$', login_required(ShipmentListView.as_view()), name='shipments'),           #all
    url(r'^myshipments/(?P<pk>\d+)/$', ShipmentDetailView.as_view(), name='shipment_detail'),       #one
    url(r'^myshipments/(?P<shipment_id>\d+)/send/$', login_required('email_fruitcake'), name='send_fruitcake'),     #send
    
   
    url(r'^upload/$', 'upload_file', name='myfruitcake_upload'),
    url(r'^about/$', 'about', name='about'),
#    url(r'^success/$', 'success', name='myfruitcake_success'),

    url(r'^path/.*$', 'path', name='path'),
    url(r'^meta/.*$', 'meta', name='meta'),
#    url(r'^search-form/$', 'search_form', name='myfruitcake_search_form'),
    url(r'^search/$', 'search', name='search'),
    #url(r'^map/$', 'testmap', name='testmap'),
#    url(r'^duplicate/$', 'duplicate', name='myfruitcake_duplicate'),
) 


