from django import forms
from registration.models import RegistrationProfile
import os
from fruitcakesite.settings import MEDIA_ROOT

from datetime import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse

from django.utils import unittest
from django.test.utils import setup_test_environment
setup_test_environment()

from django.test import TestCase
from django.test.client import Client
from django.core import mail
from django.contrib.auth.models import User, UserManager
from django.contrib.sites.models import Site

from myfruitcake.models import Fruitcake, Shipment, IPAddress, Like, Upload, EmailContact

from django.contrib.gis.geoip import GeoIP
geoip = GeoIP()

class IPAddresMethodTests(TestCase):
    def setUp(self):
        ip = IPAddress(ipaddress='184.76.1.84')

    def test_get_city_from_geoIP(self):
        """
        get_city() should return 'Portland' for ipaddress 184.76.1.84
        """
        addr = '184.76.1.84'
        city = geoip.city(addr)['city']
        self.assertEqual(city==u'Portland', True)

    def test_IPAddress__unicode__(self):
        test = IPAddress(ipaddress='184.76.1.84')
        self.assertEqual(test.__unicode__(), '184.76.1.84')
        self.assertEqual(test.get_city()['city'], u'Portland')

class EmailContactTestCase(TestCase):
    def setUp(self):
        EmailContact.objects.create(email='support@justfruitcake.com')

    def test_EmailContact_has_email(self):
        contact = EmailContact.objects.get(email='support@justfruitcake.com')
        self.assertEqual(contact.email, 'support@justfruitcake.com')
        self.assertEqual(contact.__unicode__(), 'support@justfruitcake.com')

class NewFruitcakeTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='ak', password='pwd', email='ak@justfruitcake.com')
        #f = Fruitcake.objects.create(pic='pics/241435229994408022_DoszNqwg_b_1.jpg', popup='This is a test', uploader_id=30, dt=datetime.now())

    def content_test(self, url, values):
        """Get content of url and test that each of items in `values` list is present."""
        r = self.c.get(url)
        self.assertEquals(r.status_code, 200)
        for v in values:
            self.assertTrue(v in r.content)

    def test_get_upload_file_form(self):
        self.c = Client()
        self.c.login(username='ak', password='pwd')
        r = self.c.get('/upload/', follow=True)
        self.assertEqual(r.status_code, 200)
        #r = self.c.post('/registration/login/login/', {'username': 'ak', 'password': 'pwd'}, follow=True)
        #r = self.c.get('/myfruitcake/')
        #self.assertTrue('photo?' in r.content)

class FruitcakeTestCase(TestCase):
    """
    def setUp(self):
        f = Fruitcake.objects.create(pic='pics/241435229994408022_DoszNqwg_b_1.jpg', popup='This is a test', uploader_id=30, dt=datetime.now())
    """

    def test_login(self):
        c = Client()
        response = c.post('/registration/login/?next=/myfruitcake/', {'username': 'fred', 'password': 'gobbledygook'})
        self.assertEqual(response.status_code, 200)
   
    def test_login_fail_w_blank_password(self):
        c = Client()
        response = c.post('/registration/login/?next=/myfruitcake/', {'username': 'fred', 'password': ''})
        self.assertEqual(response.status_code, 200)

    """
    def test_fruitcake_exists(self):
        self.assertEqual(self.f.pic, 'pics/241435229994408022_DoszNqwg_b_1.jpg')
    """

    def test_create_user_and_activate_and_ship_fruitcake(self):
        """ TODO: too much in here; reduce it.
        test create_logged_in_user and send activation email.
        Create one user, then try to create another on the same username (should fail), then on the same email address (should fail), then send a fruitcake from the first user.
        """
        # Credentials to use
        pwd = 'Sp8rky=4242'
        username = 'lucy'
        email = 'lucy@lucyricky.com'
       
        # Register user
        resp = self.client.post(reverse('registration_register'),
                data={'username' : username,
                      'email'    : email,
                      'password1': pwd,
                      'password2': pwd})
        self.assertRedirects(resp, reverse('registration_complete'))

        # Get the new user and check username, pwd, email, not yet activated,
        #  and activation email sent
        new_user = User.objects.get(username=username)
        self.failUnless(new_user.check_password(pwd))
        self.assertEqual(new_user.email, email)
        self.failIf(new_user.is_active)
        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

        # Test activation
        #import pydevd; pydevd.settrace()
        
        profile = RegistrationProfile.objects.get(user__username=username)
        resp = self.client.get(reverse('registration_activate',
                                       kwargs={'activation_key': profile.activation_key}))
        print "After getting reverse('registration_activate'), redirecting to: %s" % (resp)
        self.assertRedirects(resp, reverse('registration_activation_complete'))

        mypath = '/home/fisk/Desktop/fruitcake_pinterest_more/'
        myfile = '2ef7bcf22a6564a342f41ff827643477.jpg'
        mypopup = "Pick me! I'm super tasty!"

        # For image file upload, open as rb and add file name to post
        f = open(''.join([mypath, myfile]), "rb" )
        #thumbnail = '/'.join(['thumbnails', myfile])
        #pic = '/'.join(['pics', myfile])
        #print "New user info: %s %d" % (new_user.username, new_user.id)
        resp = self.client.post(reverse('myfruitcake_upload'), {'name': myfile, 'pic': f, 'uploader': new_user.id, 'popup': mypopup})
        #f.close()
        print "After upload, redirecting to: %s" % (resp)
        #self.assertRedirects(resp, reverse('myfruitcake') )
        print resp.status_code
        #self.assertEqual( (myfile in os.listdir(''.join([MEDIA_ROOT, 'pics']))), 1)
            
        # Ship a fruitcake
        ##u = User.objects.get(username='lucy')
        ##print "User %s has id %d" % (u.username, u.id)
        """
        s = Shipment.objects.create(dt=datetime.now(), fruitcake_id=f.id, sender_id=u.id,message="Hey there, this is a fine fruitcake!")
        self.assertEqual(s.message, "Hey there, this is a fine fruitcake!")
        self.assertEqual(len(mail.outbox), 1)
        """

    def test_upload_fruitcake(self):
        """
        print "Test upload goes here"
        """
        # Test if can still log in as user created above


    def test_create_fruitcake(self):
        """
        test_create_fruitcake should create a fruitcake with a popup
        """
        """
        c = Client()
        response = c.post('/registration/login/?next=/myfruitcake/', {'username': 'fred', 'password': ''})
 
        f = Fruitcake.objects.create(pic="pics/2ef7bcf22a6564a342f41ff827643477.jpg", uploader_id="30", dt=datetime.now(), times_shipped=0, popup=u"Pick me! I'm tasty")
        self.assertEqual(f.popup, "Pick me! I'm tasty")
        """

    def test_create_shipment(self):
        """
        test_create_shipment should create a shipment with a shipment message
        """
        """
        #print "%d %d" % (f.id, f.uploader_id)
        s = Shipment.objects.create(dt=datetime.now(), fruitcake_id=f.id, sender_id=f.uploader_id,message="Hey there, this is a fine fruitcake!")
        self.assertEqual(s.message, "Hey there, this is a fine fruitcake!")
        """

class EmailTest(TestCase):
    
    def test_send_activation_email(self):
        """ test send activation email tests whether an email goes into the outbox
        """
        """
        mail.send_mail('Subject here', 'Here is the message', 'from@example.com', 
                ['to@example.com'], fail_silently=False)
        
        self.assertEqual(len(mail.outbox), 1)
        """
