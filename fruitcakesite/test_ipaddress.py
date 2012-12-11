from django.db import models

from django.contrib.gis.geoip import GeoIP
g = GeoIP()

s1 = '67.168.194.54'
s2 = '201.124.105.183'
s3 = '173.45.243.93'
s4 = '70.102.23.162'

class IPAddress(models.Model):
    ipaddress = models.GenericIPAddressField(default='255.255.255.255')  # GeoIP returns None for this address
    city = models.CharField(max_length=60, null=True)
    region = models.CharField(max_length=30, null=True)
    country = models.CharField(max_length=50, null=True)
    country_code = models.CharField(max_length=2, null=True)

    class Meta:
        app_label = 'test'

    def __unicode__(self):
        return unicode(self.ipaddress)

    def __init__(self, *args, **kwargs):
        super(IPAddress, self).__init__(*args, **kwargs)
        

    def get_city(self):
        # Returns a dict with area_code, city, country_code, country_name, 
        # country_code3 (abbrev), region, postal_code, latitude, longitude, and dma_code
        return geoip.city(self.ipaddress)


