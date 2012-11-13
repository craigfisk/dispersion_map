from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
#from django.db.models.signals import post_save
from django.core.files import File
from os.path import join as pjoin
from tempfile import *
from PIL import Image as PImage
from fruitcakesite.settings import MEDIA_ROOT, MEDIA_URL, WIDTH_AVATAR, WIDTH_FRUITCAKE

class Fruitcake(models.Model):
    thumbnail = models.ImageField("Thumbnail Pic", upload_to='thumbnails', blank=True, null=True)
    pic = models.ImageField("Regular Pic", upload_to='pics', blank=False, null=False)
    popup = models.CharField(max_length=256, blank=True, null=True)
    source = models.URLField(max_length=200, blank=True, null=True)
    #CF20121107: use quotes around Shipment and Upload in next 2 lines because classes not defined until below
    shipments = models.ManyToManyField('Shipment', related_name='shipments',verbose_name='shipments')
    uploads = models.ManyToManyField('Upload', related_name='uploads', verbose_name='uploads')
    uploader = models.ForeignKey(User)

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

class Likes(models.Model):
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

class Shipment(models.Model):
    dt = models.DateTimeField(auto_now_add=True) 
    fruitcake = models.ForeignKey(Fruitcake)
    sender = models.ForeignKey(User, verbose_name='senders', related_name='senders')
    receiver = models.ManyToManyField(User, verbose_name='addressees', related_name='receivers')

    def __unicode__(self):
        return unicode(self.dt)


### Admin
class FruitcakeAdmin(admin.ModelAdmin):
    list_display = ['thumbnail']

class UploadAdmin(admin.ModelAdmin):
    pass

class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['dt', 'fruitcake', 'sender', 'receiver']

