from django.db import models
from django.contrib.auth.models import User
#from django.db.models.signals import post_save
from django.core.files import File
from os.path import join as pjoin
from tempfile import *
from PIL import Image as PImage
from fruitcakesite.settings import MEDIA_ROOT, MEDIA_URL, WIDTH_AVATAR, WIDTH_FRUITCAKE
from django.contrib.gis.geoip import GeoIP

geoip = GeoIP()

class Fruitcake(models.Model):
    dt = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField("Thumbnail Pic", upload_to='thumbnails', blank=True, null=True)
    pic = models.ImageField("Regular Pic", upload_to='pics', blank=False, null=False)
    popup = models.CharField(max_length=256, blank=True, null=True)
    source = models.URLField(max_length=200, blank=True, null=True)
    #CF20121107: use quotes around Shipment and Upload in next 2 lines because classes not defined until below
    shipments = models.ManyToManyField('Shipment', related_name='shipments',verbose_name='shipments')
    uploads = models.ManyToManyField('Upload', related_name='uploads', verbose_name='uploads')
    uploader = models.ForeignKey(User)
    likes = models.ManyToManyField('Like', related_name='likes', verbose_name='likes', blank=True, null=True)

    def __unicode__(self):
        return unicode(self.pic)

    #CF20121107  todo; compare forum.Post.profile_data()
    """
    def fruitcake_data(self): 
        uploads = self.uploads.upload_set.count()
        shipments = self.shipments.shipment_set.count()
        return uploads, shipments
    """
    # Resize to standard width during save()
    def save(self, *args, **kwargs):
        super(Fruitcake, self).save(*args, **kwargs)
        # self.pic.name <-- self.name; otherwise error: ImageFieldFile has no attribute 'startswith'
        imfn = pjoin(MEDIA_ROOT, self.pic.name)
        im = PImage.open(imfn)
        wpercent = (WIDTH_FRUITCAKE/float(im.size[0]))
        hsize = int((float(im.size[1])*float(wpercent)))
        im = im.resize((WIDTH_FRUITCAKE, hsize), PImage.ANTIALIAS)
        im.save(imfn, "JPEG") 

CHOICES = (
        (None, "Like?"),
        (True, "Like"),
        (False, "Dislike")
        )

class Like(models.Model):
    dt = models.DateTimeField(auto_now_add=True)
    like = models.NullBooleanField(choices = CHOICES, default=None)
    fruitcake = models.ManyToManyField(Fruitcake)
    user = models.ManyToManyField(User)

class Upload(models.Model):
    dt = models.DateTimeField(auto_now_add=True) 
    fruitcake = models.ForeignKey(Fruitcake)
    uploader = models.OneToOneField(User)

    def __unicode__(self):
        return unicode(self.dt)

class EmailContact(models.Model):
    email = models.EmailField(max_length=256, blank=False, null=False)

    def __unicode__(self):
        return unicode(self.email)

class IPAddress(models.Model):
    ipaddress = models.GenericIPAddressField(default='255.255.255.255')  # GeoIP returns None for this address
    city = models.CharField(max_length=60, null=True)
    region = models.CharField(max_length=30, null=True)
    country_name = models.CharField(max_length=50, null=True)
    country_code = models.CharField(max_length=2, null=True)

    def __unicode__(self):
        return unicode(self.ipaddress)

    def get_city(self):
        # Returns a dict with area_code, city, country_code, country_name, 
        # country_code3 (abbrev), region, postal_code, latitude, longitude, and dma_code
        return geoip.city(self.ipaddress)

class Shipment(models.Model):
    dt = models.DateTimeField(auto_now_add=True)
    origin = models.ForeignKey('Shipment', null=True, related_name='shipment_origin')
    parent = models.ForeignKey('Shipment', null=True, related_name='shipment_parent')
    fruitcake = models.ForeignKey(Fruitcake)
    sender = models.ForeignKey(User, verbose_name='senders', related_name='senders')
    emailcontacts = models.ManyToManyField('EmailContact', related_name='emailcontacts',verbose_name='emailcontacts', null=True)
    ipaddresses = models.ManyToManyField('IPAddress', related_name='ipaddresses', verbose_name='ipaddresses', null=True)
    message = models.TextField(max_length=2048, blank=False, null=False)
    text = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.id)

    def get_shipment_list(self):
        shipment_list = Shipment.objects.filter(origin=self.origin).order_by('-dt')
        return shipment_list


