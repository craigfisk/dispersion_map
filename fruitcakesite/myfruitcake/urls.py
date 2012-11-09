from django.views.generic import DetailView, ListView, TemplateView
from myfruitcake.models import Fruitcake, Upload, Shipment
from myfruitcake.views import activity, upload_file, FruitcakeListView
from django.conf.urls import patterns, include, url

urlpatterns = patterns('myfruitcake.views',
#    url(r"", "main"),
    url(r'^$', FruitcakeListView.as_view(model=Fruitcake)),
#    url(r'^upload/$', 'upload_file'),
)
