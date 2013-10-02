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

    def test_get_city(self):
        """
        get_city() should return 'Portland' for ipaddress 184.76.1.84
        """
        addr = '184.76.1.84'
        city = geoip.city(addr)['city']
        self.assertEqual(city==u'Portland', True)


class FruitcakeTestCase(TestCase):
 
    def test_random(self):
        print "This is a random test"

    def test_login(self):
        c = Client()
        response = c.post('/registration/login/?next=/myfruitcake/', {'username': 'fred', 'password': 'gobbledygook'})
        self.assertEqual(response.status_code, 200)
   
    def test_login_fail_w_blank_password(self):
        c = Client()
        response = c.post('/registration/login/?next=/myfruitcake/', {'username': 'fred', 'password': ''})
        self.assertEqual(response.status_code, 200)
 
    def test_create_logged_in_user(self):
        """ test create_logged_in_user and send activation email.
        first goes to /registration/login/register/?next=/registration/registration_complete/
        """
        c = Client()
        pwd = 'Sp8rky=4242'

        username = 'lucy'
        email = 'lucy@lucyricky.com'
        response = c.post('/registration/login/register/?next=/registration/registration_complete/',
                {'username': username, 'email': email ,'password': pwd, 'password2': pwd})
        print "Status code: %d for: %s" % (response.status_code, username)
        self.assertEqual(response.status_code, 200)

        username = 'ricky'
        email = 'ricky@lucyricky.com'
        user = User.objects.create_user(username, email, pwd)
        # Now see if we can log in on the same credentials
        self.assertEqual(c.login(username=username, password=pwd), True)

        """
        print "Since the mail.outbox is emptied at the start of every TestCase..."
        print "Ok, first time: email in the mail.outbox: %d" % (len(mail.outbox))
        print "Now see if we can login with this user"

        result = c.login(username='wcf1', password='Sp8rky=4242')
        if result:
            print 'Logged in ok with newly-created user wcf1 and password'
        else:
            print 'Failed to log in'
        """
        # submit

        # goes to http://127.0.0.1:8000/registration/login/register/complete/

    def test_upload_fruitcake(self):
        print "Test upload goes here"

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
        print "%d %d" % (f.id, f.uploader_id)
        s = Shipment.objects.create(dt=datetime.now(), fruitcake_id=f.id, sender_id=f.uploader_id,message="Hey there, this is a fine fruitcake!")
        self.assertEqual(s.message, "Hey there, this is a fine fruitcake!")
        """

class EmailTest(TestCase):
    
    def test_send_activation_email(self):
        # Send a message on locmem
        mail.send_mail('Subject here', 'Here is the message', 'from@example.com', ['to@example.com'], fail_silently=False)
        
        self.assertEqual(len(mail.outbox), 1)
        for item in mail.outbox:
            print "Type of the outbox item is: %s" % (type(mail.outbox[0]))

        print "Ok, second time: email in the mail.outbox: %d" % (len(mail.outbox))

