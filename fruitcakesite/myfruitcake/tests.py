import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from myfruitcake.models import Fruitcake, IPAddress
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
