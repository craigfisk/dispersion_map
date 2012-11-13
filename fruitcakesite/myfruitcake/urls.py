from django.views.generic import DetailView, ListView, TemplateView
from myfruitcake.models import Fruitcake, Upload, Shipment
from myfruitcake.views import activity, upload_file, FruitcakeListView
#, MyFruitcakeListView
from django.conf.urls import patterns, include, url

from django.contrib.auth.decorators import login_required

urlpatterns = patterns('myfruitcake.views',
#    url(r"", "main"),
#    url(r'^$', login_required(FruitcakeListView.as_view(model=Fruitcake))),
    url(r'^$', FruitcakeListView.as_view(model=Fruitcake), name='fruitcakelistview'),
    url(r'^upload/$', 'upload_file'),
    url(r'^success/$', 'success'),
#    url(r'^myuploads/$', login_required(MyFruitcakeListView.as_view(model=Fruitcake)))
)
