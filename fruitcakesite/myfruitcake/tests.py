# -*- coding: utf-8 -*-

#from django import forms
#from registration.models import RegistrationProfile
import os
import re
from os.path import join as pjoin
from fruitcakesite.settings import MEDIA_ROOT, CF_HOME_IP

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

from myfruitcake.models import Fruitcake, IPAddress, Shipment, Upload, EmailContact #, Like
from django.core.exceptions import ValidationError
from django.core import mail

from django.contrib.gis.geoip import GeoIP
geoip = GeoIP()


class MyfruitcakeTestCase(TestCase):
    #fixtures = ['contenttypes.json', 'auth.json', 'registration.json', 'myfruitcake.json',]
    
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='pwd', email='admin@justfruitcake.com')
        self.user = User.objects.create_user(username='cf', password='pwd', email='support@justfruitcake.com')
        self.otheruser = User.objects.create_user(username='fred', password='pwd', email='fred@justfruitcake.com')

     
    def content_test(self, url, values):
        """Get content of url and test that each of items in `values` list is present."""
        r = self.c.get(url)
        self.assertEquals(r.status_code, 200)
        for v in values:
            self.assertTrue(v in r.content)

    def remove_test_files(self, subdirectory, pattern):
        somedir = pjoin(MEDIA_ROOT, subdirectory)
        names = os.listdir(somedir)
        f_re = re.compile(pattern)
        for name in names:
            for m in f_re.finditer(name):
                if m: os.unlink( pjoin(somedir, m.group()) )
        
    def test_list_all_fruitcake(self):
        r = self.client.get( reverse('fruitcakelistview'))
        self.assertEqual(r.status_code, 200)
    
    def test_get_upload_fruitcake_and_ship_it(self):
        self.c = Client()

        # Anonymous visit to home should return "sign-in"
        r = self.c.get('/')
        self.assertTrue('sign-in' in r.content)

        loggedin = self.c.login(username='cf', password='pwd')

        # Logged-in visit to home should return "sign-out"
        r = self.c.get('/')
        self.assertTrue('sign-out' in r.content)

        testfruitcakepath = 'images/380277419_d6a8864724.jpg'
        picpath = pjoin(MEDIA_ROOT, ('pics/' + testfruitcakepath) )
        thumbpath = pjoin(MEDIA_ROOT, ('thumbnails/' + testfruitcakepath) )


        r = self.c.get('/myfruitcake/')
        self.assertTrue("Upload a fruitcake" in r.content)

        ##testnonjpegpath = 'testnonjpeg.png'
        self.remove_test_files("pics", r"testfruitcake_?\d*\..*$")
        self.remove_test_files("thumbnails", r"testfruitcake_?\d*\..*$")

        try:
            # Can we get the upload form page?
            r = self.c.get('/myfruitcake/upload/', follow=True)
            self.assertEqual(r.status_code, 200)
            # Can we upload a fruitcake using it?
            imfn = pjoin(MEDIA_ROOT, testfruitcakepath)
            with open(imfn) as fp:
                r = self.c.post('/myfruitcake/upload/?next=/myfruitcake/', {'pic': fp, 'popup': 'Tasty!'}, follow=True)
            self.assertEqual(r.status_code, 200)

            # Test upload

            # Are we prevented from uploading the same file again from this user?
            imfn = pjoin(MEDIA_ROOT, testfruitcakepath)
            with open(imfn) as fp:
                r = self.c.post('/myfruitcake/upload/?next=/myfruitcake/', {'pic': fp, 'popup': 'Tasty!'}, follow=True)
            self.assertTrue('already uploaded' in r.content)
            
            # Has the fruitcake been uploaded to the correct locations? 
           
            self.assertEqual(os.path.exists(picpath), True)
            self.assertEqual(os.path.exists(picpath), True)

            # Send the new fruitcake (should be only the 1 that we just uploaded; uploader_id=f.id=1)
            f = Fruitcake.objects.get(uploader_id=self.user.id)
            r = self.c.get(('/myfruitcake/'+ str(f.id) + '/shipment/'))

            #Note: sending from test user to 1 address (actually, to the test user)
            email_string = self.user.email
            r = self.c.post(('/myfruitcake/' + str(f.id) + '/shipment/'), {'email': email_string, 'message':'Hi there!'}, follow=True)
            self.assertTrue('Sent!' in r.content)

            # Send it to 2 addresses (should hit 1 on to:, 1 in bcc:)
            email_string = self.user.email + ' ' + 'wcraigfisk@gmail.com'
            r = self.c.post(('/myfruitcake/' + str(f.id) + '/shipment/'), {'email': email_string, 'message':'Hi there!'}, follow=True)
            self.assertTrue('Sent!' in r.content)

            # Do something wrong with the email string, like put a semicolon between
            email_string = self.user.email + ' / ' + 'wcraigfisk@gmail.com'
            #with self.assertRaises(ValidationError):
            r = self.c.post(('/myfruitcake/' + str(f.id) + '/shipment/'), {'email': email_string, 'message':'Hi there!'}, follow=True)
           
            # Send to a blank email address
            email_string = ''
            r = self.c.post(('/myfruitcake/' + str(f.id) + '/shipment/'), {'email': email_string, 'message':'Hi there!'}, follow=True)
            self.assertTrue('Sent!' not in r.content)

            # bad email address 
            email_string = '1@67'
            r = self.c.post(('/myfruitcake/' + str(f.id) + '/shipment/'), {'email': email_string, 'message':'Hi there!'}, follow=True)
            self.assertTrue('Sent!' not in r.content)

            # The following 2 will fail currently but later may not fail
            # 1) international email address - see Wikipedia on "email address"
            email_string = 'Pelé@example.com'
            r = self.c.post(('/myfruitcake/' + str(f.id) + '/shipment/'), {'email': email_string, 'message':'Hi there!'}, follow=True)
            self.assertTrue('Sent!' not in r.content)

            # 2) international email address - see Wikipedia on "email address"
            email_string = '甲斐@黒川.日本'
            r = self.c.post(('/myfruitcake/' + str(f.id) + '/shipment/'), {'email': email_string, 'message':'Hi there!'}, follow=True)
            self.assertTrue('Sent!' not in r.content)

            # check shipment list from the data
            self.s = Shipment.objects.get(pk=1)
            shipment_list = self.s.get_shipment_list()
            self.assertEqual(len(shipment_list), 1)
           
            # check shipment list from the web
            r = self.c.get('/myfruitcake/myshipments/')
            self.assertTrue('Listing of fruitcake' in r.content)

            # Access the shipment and send it on again
            r = self.c.post('/myfruitcake/2/shipment/', {'email': 'support@justfruitcake.com', 'message': 'Here it goes again!'})
            self.assertTrue(r.status_code, 200)
            self.assertTrue('Click to continue' in r.content) # Note: This may change

            # Access the shipment and send it on a third time
            r = self.c.post('/myfruitcake/2/shipment/', {'email': 'support@justfruitcake.com', 'message': 'Here it goes a third time!'})
            self.assertTrue(r.status_code, 200)
            self.assertTrue('Click to continue' in r.content) # Note: This may change


            # Test __unicode__() responses for various objects
            # class Upload
            u = Upload.objects.create(dt=datetime.utcnow(), fruitcake=f, uploader = self.user)
            currentdate = unicode(datetime.date(datetime.utcnow()))
            self.assertTrue(u.__unicode__().startswith(currentdate))
            # class Shipment
            self.assertEqual(self.s.__unicode__(), unicode(1) )
            # class EmailContact
            e = EmailContact(email=self.user.email)
            self.assertEqual(e.__unicode__(), self.user.email)
            
           
            ## Note: 3 methods of Shipment are commented out and not used in view.py
            ##latest_shipments = self.s.latest_shipment()
            ##self.assertEqual(len(latest_shipments), 1)
            ##parent_list = self.s.get_parent_list()
            ##self.assertEqual(parent_list, None)
            #latest_shipment = Shipment.objects.get(pk=1)
            ##self.assertEqual(Shipment.objects.count(), 1)

        except IOError as e:
            print "Unable to open file: %s" % e
        
        finally:
            print "\nCleaning up\n"

            # Can we get rid of the test fruitcake?
            if os.path.exists(picpath):
                os.unlink(picpath)
            if os.path.exists(thumbpath):
                os.unlink(thumbpath)
            self.assertEqual(os.path.exists(picpath), False)
            self.assertEqual(os.path.exists(picpath), False)

            #self.assertEqual(f.__unicode__(), pjoin('pics', testfruitcakepath) )

            self.c.logout()

    def test_admin_login(self):
        self.c = Client()
        loggedin = self.c.login(username='admin', password='pwd')
        r = self.c.get('/admin/')
        r.status_code
        self.assertEqual(r.status_code, 200)
        
        testfruitcakepath = 'images/380277419_d6a8864724.jpg'
        picpath = pjoin(MEDIA_ROOT, ('pics/' + testfruitcakepath) )
        thumbpath = pjoin(MEDIA_ROOT, ('thumbnails/' + testfruitcakepath) )

        r = self.c.get('/myfruitcake/path/')
        self.assertEqual(r.status_code, 200)
        r = self.c.get('/myfruitcake/meta/')
        self.assertEqual(r.status_code, 200)
        r = self.c.get('/myfruitcake/search/')
        self.assertEqual(r.status_code, 200)
        # Upload a fruitcake for the admin
        #testfruitcakepath = 'testfruitcake.jpg'
        ##testnonjpegpath = 'testnonjpeg.png'
        self.remove_test_files("pics", r"testfruitcake_?\d*\..*$")
        self.remove_test_files("thumbnails", r"testfruitcake_?\d*\..*$")

        try:
            # Can we get the upload form page?
            r = self.c.get('/myfruitcake/upload/', follow=True)
            self.assertEqual(r.status_code, 200)
            # Can we upload a fruitcake using it?
            imfn = pjoin(MEDIA_ROOT, testfruitcakepath)
            with open(imfn) as fp:
                r = self.c.post('/myfruitcake/upload/?next=/myfruitcake/', {'pic': fp, 'popup': 'Tasty as can be!'}, follow=True)
            self.assertEqual(r.status_code, 200)

            # Has the fruitcake been uploaded to the correct locations? 
            picpath = pjoin(MEDIA_ROOT, ('pics/' + testfruitcakepath) )
            thumbpath = pjoin(MEDIA_ROOT, ('thumbnails/' + testfruitcakepath) )
            
            self.assertEqual(os.path.exists(picpath), True)
            self.assertEqual(os.path.exists(picpath), True)

            # Send the new fruitcake (should be only the 1 that we just uploaded; uploader_id=f.id=1)
            f = Fruitcake.objects.get(uploader_id=self.admin.id)
 
        except IOError as e:
            print "Unable to open file: %s" % e
        
        finally:
            print "\nCleaning up\n"

            # Can we get rid of the test fruitcake?
            if os.path.exists(picpath):
                os.unlink(picpath)
            if os.path.exists(thumbpath):
                os.unlink(thumbpath)
            self.assertEqual(os.path.exists(picpath), False)
            self.assertEqual(os.path.exists(picpath), False)
       
        # Normal search with one search term
        r = self.c.get('/myfruitcake/search/', {'q':'Tasty'})
        self.assertEqual(r.status_code, 200)
        b = self.assertTrue('Tasty' in r.content)
        
        # Search term is not going to be found
        r = self.c.get('/myfruitcake/search/', {'q':'Rabbits'})
        self.assertEqual(r.status_code, 200)
        #b = self.assertTrue('Tasty' in r.content)
 
        # Try a blank
        r = self.c.get('/myfruitcake/search/', {'q':''})
        self.assertEqual(r.status_code, 200)
        self.assertTrue('Please enter a search term' in r.content)

        # Search term is too long
        r = self.c.get('/myfruitcake/search/', {'q':'This is a very long and rambling search term'})
        self.assertEqual(r.status_code, 200)
        self.assertTrue('Please enter at most 20 characters' in r.content)

        self.c.logout()
        
class IPAddresMethodTests(TestCase):
    def setUp(self):
        ip = IPAddress(ipaddress=CF_HOME_IP)

    def test_get_city_from_geoIP(self):
        """
        get_city() should return 'Portland' for ipaddress CF_HOME_IP
        """
        addr = CF_HOME_IP
        city = geoip.city(addr)['city']
        self.assertEqual(city==u'Portland', True)

    def test_IPAddress__unicode__(self):
        test = IPAddress(ipaddress=CF_HOME_IP)
        self.assertEqual(test.__unicode__(), CF_HOME_IP)
        self.assertEqual(test.get_city()['city'], u'Portland')


