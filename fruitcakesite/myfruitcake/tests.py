#from django import forms
#from registration.models import RegistrationProfile
import os
from fruitcakesite.settings import MEDIA_ROOT

from datetime import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse

#from django.utils import unittest
#from django.test.utils import setup_test_environment
#setup_test_environment()

from django.test import TestCase
from django.test.client import Client
#from django.core import mail
from django.contrib.auth.models import User #, UserManager
#from django.contrib.sites.models import Site

from myfruitcake.models import Fruitcake, IPAddress # Shipment, Upload, EmailContact, Like

from django.contrib.gis.geoip import GeoIP
geoip = GeoIP()

class NewFruitcakeTestCase(TestCase):
    #fixtures = ['contenttypes.json', 'auth.json', 'registration.json', 'myfruitcake.json',]
    
    def setUp(self):
        self.user = User.objects.create_user(username='ak', password='pwd', email='ak@justfruitcake.com')
        #f = Fruitcake.objects.create(pic='pics/241435229994408022_DoszNqwg_b_1.jpg', popup='This is a test', uploader_id=30, dt=datetime.now())

    def content_test(self, url, values):
        """Get content of url and test that each of items in `values` list is present."""
        r = self.c.get(url)
        self.assertEquals(r.status_code, 200)
        for v in values:
            self.assertTrue(v in r.content)

    def test_get_upload_file_form(self):
        self.c = Client()
        a = self.c.login(username=self.user.username, password='pwd')

#        b = self.c.login(username='ak', password='pwd')
        #r = self.c.post('/registration/login/login/', {'username': 'ak', 'password': 'pwd'}, follow=True)
        #r = self.c.get('/myfruitcake/')
        #self.assertTrue('photo?' in r.content)

        testfruitcakepath = 'testfruitcake.jpg'
        self.assertEqual(testfruitcakepath, 'testfruitcake.jpg')
        r = self.c.get('/myfruitcake/upload/', follow=True)
        self.assertEqual(r.status_code, 200)
        r = self.c.post('/myfruitcake/upload/?next=/myfruitcake/', {'pic': testfruitcakepath, 'popup': 'Tasty!'}, follow=True)
        self.assertEqual(r.status_code, 200)

