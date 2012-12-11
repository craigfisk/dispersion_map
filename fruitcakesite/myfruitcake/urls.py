from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, TemplateView
from myfruitcake.models import Fruitcake, Upload, Shipment
from myfruitcake.views import activity, upload_file, MyFruitcakeListView, ShipmentListView, ShipmentDetailView, email_fruitcake
from fruitcakesite.views import FruitcakeListView
#ShipmentListView, email_fruitcake
#, ShipmentDetailView
#EmailTemplateView, e
#, MyFruitcakeListView
from django.conf.urls import patterns, include, url

from django.contrib.auth.decorators import login_required

urlpatterns = patterns('myfruitcake.views',
#    url(r"", "main"),
#    url(r'^$', login_required(FruitcakeListView.as_view(model=Fruitcake))),
    url(r'^$', MyFruitcakeListView.as_view(model=Fruitcake), name='myfruitcakelistview'),

    url(r'^myshipments', ShipmentListView.as_view(model=Shipment), name='myshipments'),
    url(r'^upload/$', 'upload_file'),
    url(r'^success/$', 'success'),
#    url(r'^email/(?P<fruitcake_id>\d+)/$', 'email_fruitcake'),
#    url(r'^email/(?P<fruitcake_id>\d+)/shipment/(?P<shipment_id>\d+)/$', 'email_fruitcake'),

    #url(r'^(?P<fruitcake_id>\d+)/shipment/$', 'email_fruitcake'),
    url(r'(?P<fruitcake_id>\d+)/shipment/$', 'email_fruitcake'),
    url(r'^(?P<fruitcake_id>\d+)/shipment/(?P<shipment_id>\d+)/$', 'email_fruitcake'),
   
#    url(r'^email/(?P<fruitcake_id>\d+)/shipment/(?P<shipment_id>\d+)/$', ShipmentDetailView.as_view(model=Shipment), name='address_email'),
#    url(r'^shipment/(?P<pk>\d+)/$', ShipmentDetailView.as_view(model=Shipment)),
#    url(r'^shipment/(?P<pk>\d+)/$', 'regift_fruitcake'),
#    url(r'^email/$', 'email_fruitcake'),
#    url(r'^email/(\d+)/$', EmailTemplateView.as_view(model=Fruitcake), name='emailtemplateview'), 
#    url(r'^myuploads/$', login_required(MyFruitcakeListView.as_view(model=Fruitcake)))
    url(r'^path/.*$', 'path'),
    url(r'^meta/.*$', 'meta'),
    url(r'^search-form/$', 'search_form'),
    url(r'^search/$', 'search'),
) 

"""
myfruitcake/10 = stats on fruitcake 10
myfruitcake/10/user/15/email/2 = 2nd email sent by user 15 with fruitcake 10; links to all other emails that have this
as a parent or child.

need to also do:
user/10 = stats on user 10
user/10/fruitcake
user/10/emails

"""


