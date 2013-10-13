from django.db import models
from django.contrib import auth


class WeightEntry(models.Model):
    weight = models.IntegerField(help_text='Weight in pounds')
    when = models.DateTimeField(auto_now_add=True)
    manual = models.BooleanField(default=False, help_text='Was this entry entered by hand?')

    class Meta:
        verbose_name_plural = 'Weight Entries'


class WithingsAuth(models.Model):
    user = models.OneToOneField(auth.models.User, related_name='withings_auth')
    uid = models.IntegerField(help_text='Withings User ID')
    oauth_token = models.CharField(default='', max_length=256)
    oauth_secret = models.CharField(default='', max_length=256)

    class Meta:
        verbose_name = 'Withing Authorization'

    def __unicode__(self):
        return self.user.username + ' ({0})'.format(self.uid)
