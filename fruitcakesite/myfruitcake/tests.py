import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse

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


class SimpleTest(TestCase):
    def setUp(self):
        u = User.objects.create_user("ak", "ak@abc.org", "pwd")

    def content_test(self, url, values):
        """Get content of url and test that each of items in `values` list is present."""
        r = self.c.get(url)
        self.assertEquals(r.status_code, 200)
        for v in values:
            self.assertTrue(v in r.content)

    def test(self):
        self.c = Client()
        #self.c.login(username="ak", password="pwd")
        self.c.get('registration/login/?next=/myfruitcake/')
        result = self.c.login(username='lindamagee', password='Sp8rky=4242')
        #self.content_test("/", ['Copyright 2012-2013'])
        if result:
            print "Success"
            #self.content_test("/", ['<P class="main">Most shipped fruitcake (<b>click photo to send</b>):</P>'])
        else:
            print "Login failed"

        """
        self.content_test("/forum/", ['<a href="/forum/forum/1/">forum</a>'])
        self.content_test("/forum/forum/1/", ['<a href="/forum/thread/1/">thread</a>', "ak - post"])

        self.content_test("/forum/thread/1/", ['<div class="ttitle">thread</div>', '<span class="title">post</span>', 'body <br />', 'by ak |'])
        r = self.c.post("/forum/new_thread/1/", {"subject": "thread2", "body": "body2"})
        r = self.c.post("/forum/reply/2/", {"subject": "post2", "body": "body3"})
        self.content_test("/forum/thread/2/", ['<div class="ttitle">thread2</div>',
               '<span class="title">post2</span>', 'body2 <br />', 'body3 <br />'])
        """

