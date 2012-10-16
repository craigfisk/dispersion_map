from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import date

# See on creating custom UserProfile:
# https://docs.djangoproject.com/en/1.4/topics/auth/#storing-additional-information-about-users
class UserProfile(models.Model):
    # required
    user = models.OneToOneField(User)
    # fruitcake user fields
    subscription_date = models.DateField(default=date.today())
    """
    accepted_eula = models.BooleanField()
    city = models.CharField(max_length=64)
    stateprovince = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    def get_subscription(self):
        pass
    def get_shipments(self):
        pass
    def get_logins(self):
        pass
    def get_referrals(self):
        pass


    class Meta:
        db_table = u'myaccount_userprofile'
        ordering = ['country', 'stateprovince', 'city']

    def __unicode__(self):
        return self.username
    """
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

