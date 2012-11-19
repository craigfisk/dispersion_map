from django.views.generic import DetailView, ListView, TemplateView
from myfruitcake.models import Fruitcake, Upload, Shipment
from myfruitcake.views import activity, upload_file, FruitcakeListView, email_fruitcake
#EmailTemplateView, e
#, MyFruitcakeListView
from django.conf.urls import patterns, include, url

from django.contrib.auth.decorators import login_required

urlpatterns = patterns('myfruitcake.views',
#    url(r"", "main"),
#    url(r'^$', login_required(FruitcakeListView.as_view(model=Fruitcake))),
    url(r'^$', FruitcakeListView.as_view(model=Fruitcake), name='fruitcakelistview'),
    url(r'^upload/$', 'upload_file'),
    url(r'^success/$', 'success'),
    url(r'^email/(?P<pk>\d+)/$', 'email_fruitcake'),
#    url(r'^email/$', 'email_fruitcake'),


#    url(r'^email/(\d+)/$', EmailTemplateView.as_view(model=Fruitcake), name='emailtemplateview'), 
#    url(r'^myuploads/$', login_required(MyFruitcakeListView.as_view(model=Fruitcake)))
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


