import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse

from django.test.utils import setup_test_environment
setup_test_environment()

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from myfruitcake.models import Fruitcake, Shipment, IPAddress, Like, Upload, EmailContact

from django.contrib.gis.geoip import GeoIP
geoip = GeoIP()

class IPAddresMethodTests(TestCase):

    def test_get_city(self):
        """
        get_city() should return 'Portland' for ipaddress 184.76.1.84
        """
        addr = '184.76.1.84'
        city = geoip.city(addr)['city']
        self.assertEqual(city==u'Portland', True)


class ExistingFruitcakeTest(TestCase):
    def test_fruitcake_has_popup(self):
        #user = User.objects.get(username='lindamagee')
        f = Fruitcake.objects.get(id=9)
        self.assertEqual(f.popup, u"Pick me! You'll really like me!")
        #Fruitcake.objects.create(pic="pics/2ef7bcf22a6564a342f41ff827643477.jpg", uploader_id="30", dt=, times_shipped=)

