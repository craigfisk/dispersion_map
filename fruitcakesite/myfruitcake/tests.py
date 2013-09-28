from datetime import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse

from django.test.utils import setup_test_environment
setup_test_environment()

from django.test import TestCase
from django.test.client import Client
from django.core import mail
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


class FruitcakeTestCase(TestCase):
 
    def test_random(self):
        print "This is a random test"
   
    def test_create_logged_in_user(self):
        """ test create_logged_in_user and send activation email.
        first goes to /registration/login/register/?next=/registration/registration_complete/
        """
        c = Client()
        username = 'wcf1'
        email = 'fred@gmail.com'
        response = c.post('/registration/login/register/?next=/registration/registration_complete/',
                {'username': username, 'email': email ,'password': 'Sp8rky=4242', 'password2': 'S[8rky=4242'})
        print "Your status code: %d for test user: %s" % (response.status_code, username)
        
        print "Since the mail.outbox is emptied at the start of every TestCase..."
        print "Ok, email in the mail.outbox: %d" % (len(mail.outbox))

        # submit

        # goes to http://127.0.0.1:8000/registration/login/register/complete/

    def test_upload_fruitcake(self):
        print "Test upload goes here"

    def test_create_fruitcake(self):
        """
        test_create_fruitcake should create a fruitcake with a popup
        """
        """
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

        print "Ok, email in the mail.outbox: %d" % (len(mail.outbox))

