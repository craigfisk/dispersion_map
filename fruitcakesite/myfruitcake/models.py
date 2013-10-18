from django.db import models
from django.contrib.auth.models import User
#from django.db.models.signals import post_save
#from django.core.files import File
from os.path import join as pjoin
#from tempfile import *
from PIL import Image as PImage
from fruitcakesite.settings import MEDIA_ROOT, WIDTH_STANDARD, WIDTH_THUMBNAIL 
from django.contrib.gis.geoip import GeoIP
#import re

geoip = GeoIP()

from fruitcakesite.custom import MyFileStorage
mfs = MyFileStorage()

class FruitcakeException(Exception):
    pass

class Fruitcake(models.Model):
    dt = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField("Thumbnail Pic", upload_to='thumbnails', blank=True, null=True)
    ##CF20121215 dropping the pics prefix,so just going straight to /STATIC/MEDIA
    pic = models.ImageField("Regular Pic", upload_to='pics', blank=False, null=False)
    popup = models.CharField(max_length=256, blank=True, null=True)
    source = models.URLField(max_length=200, blank=True, null=True)
    #CF20121107: use quotes around Shipment and Upload in next 2 lines because classes not defined until below
    shipments = models.ManyToManyField('Shipment', related_name='shipments',verbose_name='shipments')
    uploads = models.ManyToManyField('Upload', related_name='uploads', verbose_name='uploads')
    uploader = models.ForeignKey(User)
    likes = models.ManyToManyField('Like', related_name='likes', verbose_name='likes', blank=True, null=True)
    times_shipped = models.IntegerField(default=0)
    def __unicode__(self):
        return unicode(self.pic)
    
    class Meta:
        app_label = 'myfruitcake'

    #CF20121107  todo; compare forum.Post.profile_data()
    """
    def fruitcake_data(self): 
        uploads = self.uploads.upload_set.count()
        shipments = self.shipments.shipment_set.count()
        return uploads, shipments
    """
    """ 
    def __init__(self, *args, **kwargs):
        p = getattr(self, pic)
        thumbname = re.sub('^pics\/', 'thumbnails/', p.name)
        setattr(self, self.thumbnail.name, thumbname)
    """

    def save(self, *args, **kwargs):
        """
        Saves STANDARD and THUMBNAIL versions of uploaded image
        """
        super(Fruitcake, self).save(*args, **kwargs)
        
        # WIDTH_STANDARD:
        
        # Use self.pic.name <-- not self.name; else error: ImageFieldFile has no attribute 'startswith'
        imfn = pjoin(MEDIA_ROOT, self.pic.name)
        im = PImage.open(imfn)
        wpercent = (WIDTH_STANDARD/float(im.size[0]))
        hsize = int((float(im.size[1])*float(wpercent)))
        # Replace the image with a STANDARD-sized version of itself.
        im = im.resize((WIDTH_STANDARD, hsize), PImage.ANTIALIAS)
        # According to www.pythonware.com/library/pil/handbook/image.htm, if save() fails, "usually"  
        # IOError exception and you are responsible for removing any file(s) that may have been created.
        try:
            im.save(imfn, "JPEG")
        except IOError as e:
            raise FruitcakeException("Pic IOError: %s" % e)
        except EnvironmentError as e:
            raise FruitcakeException("Pic EnvironmentError: %s" % e)
        except BaseException as e:
            raise FruitcakeException("Pic BaseException: %s" % e)
        else:
            raise FruitcakeException("Pic image file problem")
        # WIDTH_THUMBNAIL:

        # The only thing we're doing to the model (table) is updating with name for the thumbnail
        #CF20130412: NOTE: the next line might need to go BEFORE super() above -----------------------
        imfn = pjoin(MEDIA_ROOT, self.thumbnail.name)
        wpercent = (WIDTH_THUMBNAIL/float(im.size[0]))                    #why do this twice?
        hsize = int((float(im.size[1])*float(wpercent)))
        # image.resize() returns a new image
        im2 = im.resize((WIDTH_THUMBNAIL, hsize), PImage.ANTIALIAS)       #PImage.open(imfn_thumb)
        
        try:
            im2.save(imfn, "JPEG")
        #except IOError as e:
        #    print "Error: %s" % e
        except IOError as e:
            raise FruitcakeException("Thumbnail IOError: %s" % e)
        except EnvironmentError as e:
            raise FruitcakeException("Thumbnail EnvironmentError: %s" % e)
        except BaseException as e:
            raise FruitcakeException("Thumbnail BaseException: %s" % e)
        else:
            raise FruitcakeException("Thumbnail image file problem")

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

    def __unicode__(self):
        return unicode(self.like)

    class Meta:
        app_label = 'myfruitcake'


class Upload(models.Model):
    dt = models.DateTimeField(auto_now_add=True) 
    fruitcake = models.ForeignKey(Fruitcake)
    uploader = models.OneToOneField(User)

    def __unicode__(self):
        return unicode(self.dt)

    class Meta:
        app_label = 'myfruitcake'


class EmailContact(models.Model):
    email = models.EmailField(max_length=256, blank=False, null=False)

    def __unicode__(self):
        return unicode(self.email)

    class Meta:
        app_label = 'myfruitcake'


class IPAddress(models.Model):
    ipaddress = models.GenericIPAddressField(default='255.255.255.255')  # GeoIP returns None for this address
    city = models.CharField(max_length=60, null=True)
    region = models.CharField(max_length=30, null=True)
    country_name = models.CharField(max_length=50, null=True)
    country_code = models.CharField(max_length=2, null=True)

    def __unicode__(self):
        return unicode(self.ipaddress)

    class Meta:
        app_label = 'myfruitcake'

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

    class Meta:
        app_label = 'myfruitcake'

    """
    def latest_shipment(self):
        latest_shipment = Shipment.objects.filter(sender=self.request.user).order_by('-dt')[0]
        return latest_shipment
    """

    def get_shipment_list(self):
        shipment_list = Shipment.objects.filter(origin=self.origin).order_by('-dt')
        return shipment_list
    """

    def get_parent_list(self):
        shipment_list = Shipment.objects.filter(origin=self.origin).order_by('-dt')
        mylist = []
        prior = None
        
        for shipment in shipment_list:
            if (shipment.id==shipment_list[0].id) or (prior and shipment.id==prior.parent_id):
                mylist.append(shipment.id)
                prior = shipment
            if shipment.id == prior.id:
                prior = shipment
                
        parent_list = Shipment.objects.filter(pk__in=mylist).order_by('-dt')
        return parent_list
    """
    
