from django.db import models
from django.contrib import auth

import withings

from home import settings


class WeightEntry(models.Model):
    ENTRY_SOURCES = (
        (0, 'manual'),
        (1, 'withings'),
    )

    user = models.ForeignKey(auth.models.User)
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text='Weight in pounds')
    when = models.DateTimeField()
    source = models.IntegerField(choices=ENTRY_SOURCES, help_text='Where did this datum come from?')

    class Meta:
        verbose_name_plural = 'Weight Entries'
        ordering = ['-when']

    def __unicode__(self):
        return self.user.username + ' - {0} lbs'.format(self.weight) + ' @ {0}'.format(self.when)


class WithingsAuth(models.Model):
    user = models.OneToOneField(auth.models.User, related_name='withings_auth')
    uid = models.IntegerField(help_text='Withings User ID')
    oauth_token = models.CharField(default='', max_length=256)
    oauth_secret = models.CharField(default='', max_length=256)

    class Meta:
        verbose_name = 'Withing Authorization'

    def __unicode__(self):
        return self.user.username + ' ({0})'.format(self.uid)

    def get_api_client(self):
        creds = withings.WithingsCredentials(
            consumer_key        = settings.WITHINGS_CONSUMER_KEY,
            consumer_secret     = settings.WITHINGS_CONSUMER_SECRET,
            access_token        = self.oauth_token,
            access_token_secret = self.oauth_secret,
            user_id             = self.uid)

        return withings.WithingsApi(creds)
