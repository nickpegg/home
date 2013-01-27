import datetime

from django.db import models

# Create your models here.

class Beer(models.Model):
    """
    A beer. What else are you expecting?
    
    Editable from main site
    """

    name        = models.CharField(max_length=100)
    style       = models.CharField(max_length=100, blank=True)
    recipe_url  = models.CharField(max_length=1024, blank=True)
    
    
    def __unicode__(self):
        return self.name
    
    def current_state(self):
        state = None
        last_event = None
        now = datetime.datetime.now().date()

        for event in self.event_set.order_by('date'):
            if not last_event:
                last_event = event

            if event.completed and event.date >= last_event.date:
                # In case of a date tie, go with the higher ID number
                if event.date != last_event.date or event.id > last_event.id:
                    last_event = event
                    state = event.event_type
        
        return state
    
    def is_ready(self):
        ready = False
        
        for event in self.event_set.all():
            if event.event_type == 0 and not event.is_future():
                ready = True
                break
        
        return ready
    
    def is_started(self):
        started = False
        
        for event in self.event_set.all():
            if event.event_type == 1 and not event.is_future():
                started = True
                break
            
        return started


class Event(models.Model):
    """
    Beer event (brewed, fermentation, etc.)
    
    Editable via main site
    """    
    
    TYPES = (
        (0, 'Ready'),
        (1, 'Brewed'),
        (2, 'Primary Fermentation'),
        (3, 'Secondary Fermentation'),
        (4, 'Kegged'),
        (5, 'Bottled'),
    )

    beer        = models.ForeignKey(Beer)
    fermenter   = models.ForeignKey('Fermenter', default=None, null=True, blank=True)
    event_type  = models.IntegerField(choices=TYPES)
    date        = models.DateField()
    completed   = models.BooleanField()
    
    class Meta:
        unique_together = ('beer', 'event_type')
        ordering = ['-beer', '-date', '-id']
        
    def __unicode__(self):
        return '%s - %s @ %s' % (self.beer, self.resolve_etype(), self.date)
        
    def resolve_etype(self):
        description = None
        
        for etype, desc in self.TYPES:
            if etype == self.event_type:
                description = desc
            
        return description
    
    def is_future(self):
        return self.date > datetime.datetime.now().date()


class Tap(models.Model):
    """
    Kegerator tap

    Must be edited via admin site
    """
    
    number  = models.IntegerField(primary_key=True)
    beer    = models.ForeignKey(Beer, null=True, blank=True)

    def __unicode__(self):
        return 'Tap #' + str(self.number)

class Fermenter(models.Model):
    """
    Fermentation vessel
    
    Must be edited via admin site
    """

    description = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.description
