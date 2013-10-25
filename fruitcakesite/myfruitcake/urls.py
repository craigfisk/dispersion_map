from myfruitcake.models import Fruitcake, Shipment 
from myfruitcake.views import MyFruitcakeListView, ShipmentListView
from django.conf.urls import patterns, url  #include
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('myfruitcake.views',
    url(r'^$', login_required(MyFruitcakeListView.as_view(model=Fruitcake)), name='myfruitcake_listview'),
    #url(r'^$', MyFruitcakeListView.as_view(model=Fruitcake), name='myfruitcakelistview',
    url(r'^myshipments', login_required(ShipmentListView.as_view(model=Shipment)), name='myfruitcake_shipments'),
    url(r'^upload/$', 'upload_file', name='myfruitcake_upload'),
    url(r'^about/$', 'about', name='myfruitcake_about'),
#    url(r'^about_sample/$', 'about_sample'),
#    url(r'^success/$', 'success', name='myfruitcake_success'),
    url(r'(?P<fruitcake_id>\d+)/shipment/$', 'email_fruitcake', name='myfruitcake_email_fruitcake1'),
    url(r'^(?P<fruitcake_id>\d+)/shipment/(?P<shipment_id>\d+)/$', 'email_fruitcake', name='myfruitcake_email_fruitcake2'),
    url(r'^path/.*$', 'path', name='myfruitcake_path'),
    url(r'^meta/.*$', 'meta', name='myfruitcake_meta'),
#    url(r'^search-form/$', 'search_form', name='myfruitcake_search_form'),
    url(r'^search/$', 'search', name='myfruitcake_search'),
    url(r'^map/$', 'testmap', name='myfruitcake_testmap'),
#    url(r'^duplicate/$', 'duplicate', name='myfruitcake_duplicate'),
) 


