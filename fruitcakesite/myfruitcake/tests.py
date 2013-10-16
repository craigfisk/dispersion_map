#from django import forms
#from registration.models import RegistrationProfile
import os
from os.path import join as pjoin
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

from myfruitcake.models import Fruitcake, IPAddress, Shipment # Upload, EmailContact, Like

from django.contrib.gis.geoip import GeoIP
geoip = GeoIP()

class MyfruitcakeTestCase(TestCase):
    #fixtures = ['contenttypes.json', 'auth.json', 'registration.json', 'myfruitcake.json',]
    
    def setUp(self):
        self.user = User.objects.create_user(username='ak', password='pwd', email='ak@justfruitcake.com')

    def content_test(self, url, values):
        """Get content of url and test that each of items in `values` list is present."""
        r = self.c.get(url)
        self.assertEquals(r.status_code, 200)
        for v in values:
            self.assertTrue(v in r.content)

    def test_get_upload_fruitcake_and_ship_it(self):
        self.c = Client()
        loggedin = self.c.login(username='ak', password='pwd')

        r = self.c.get('/myfruitcake/')
        self.assertTrue("Upload a fruitcake" in r.content)

        testfruitcakepath = 'testfruitcake.jpg'
        testnonjpegpath = 'testnonjpeg.png'

        # Can we get the upload form page?
        r = self.c.get('/myfruitcake/upload/', follow=True)
        self.assertEqual(r.status_code, 200)
        # Can we upload a fruitcake using it?
        imfn = pjoin(MEDIA_ROOT, testfruitcakepath)
        with open(imfn) as fp:
            r = self.c.post('/myfruitcake/upload/?next=/myfruitcake/', {'pic': fp, 'popup': 'Tasty!'}, follow=True)
        self.assertEqual(r.status_code, 200)
        # Are we prevented from uploading a non-JPEG fruitcake
        imfn = pjoin(MEDIA_ROOT, testnonjpegpath)
        with open(imfn) as fp:
            r = self.c.post('/myfruitcake/upload/?next=/myfruitcake/', {'pic': fp, 'popup': 'Wrong kind!'}, follow=True)
        self.assertNotEqual(r.status_code, 200)

        # Has the fruitcake been uploaded to the correct locations? 
        picpath = pjoin(MEDIA_ROOT, 'pics/testfruitcake.jpg')
        thumbpath = pjoin(MEDIA_ROOT, 'thumbnails/testfruitcake.jpg')
        
        self.assertEqual(os.path.exists(picpath), True)
        self.assertEqual(os.path.exists(picpath), True)

        # Send the new fruitcake (should be only the 1 that we just uploaded; uploader_id=f.id=1)
        f = Fruitcake.objects.get(pk=1)
        r = self.c.get(('/myfruitcake/'+ str(f.id) + '/shipment/'))
        r = self.c.post(('/myfruitcake/' + str(f.id) + '/shipment/'), {'email': 'support@justfruitcake.com', 'message':'Hi there!'}, follow=True)
        self.assertTrue('Sent!' in r.content)

        self.s = Shipment.objects.get(pk=1)
        shipment_list = self.s.get_shipment_list()
        self.assertEqual(len(shipment_list), 1)
       
        ## Note: 3 methods of Shipment are commented out and not used
        ##latest_shipments = self.s.latest_shipment()
        ##self.assertEqual(len(latest_shipments), 1)
        ##parent_list = self.s.get_parent_list()
        ##self.assertEqual(parent_list, None)
        #latest_shipment = Shipment.objects.get(pk=1)
        ##self.assertEqual(Shipment.objects.count(), 1)
        
        # Can we get rid of the test fruitcake?
        if os.path.exists(picpath):
            os.unlink(picpath)
        if os.path.exists(thumbpath):
            os.unlink(thumbpath)
        self.assertEqual(os.path.exists(picpath), False)
        self.assertEqual(os.path.exists(picpath), False)


