import datetime

from tastypie import fields
from tastypie.resources import ModelResource

import models


class BeerResource(ModelResource):
    class Meta:
        queryset = models.Beer.objects.all()
        excludes = ['unreservable']


class TapResource(ModelResource):
    beer = fields.ToOneField(BeerResource, 'beer', full=True, null=True)

    class Meta:
        queryset = models.Tap.objects.all()


class UpcomingResource(ModelResource):
    # Beers not marked as ready
    beer = fields.ToOneField(BeerResource, 'beer', full=True)

    class Meta:
        queryset = models.Event.objects.filter(event_type=0).filter(completed=False) \
                         .filter(date__gte=datetime.datetime.now().date()).order_by('date')
        resource_name = 'upcoming'
