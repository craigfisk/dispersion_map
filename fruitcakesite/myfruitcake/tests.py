from datetime import datetime
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
    
    def test_create_fruitcake(self):
        """
        test_create_fruitcake should create a fruitcake with a popup
        """
        f = Fruitcake.objects.create(pic="pics/2ef7bcf22a6564a342f41ff827643477.jpg", uploader_id="30", dt=datetime.now(), times_shipped=0, popup=u"Pick me! I'm tasty")
        self.assertEqual(f.popup, "Pick me! I'm tasty")
        
    def test_create_shipment(self):
        """
        test_create_shipment should create a shipment with a shipment message
        """
        print "%d %d" % (f.id, f.uploader_id)
        s = Shipment.objects.create(dt=datetime.now(), fruitcake_id=f.id, sender_id=f.uploader_id,message="Hey there, this is a fine fruitcake!")
        self.assertEqual(s.message, "Hey there, this is a fine fruitcake!")


