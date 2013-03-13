import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.core.mail import send_mail
from django.template.loader import render_to_string


class Beer(models.Model):
    """
    A beer. What else are you expecting?
    
    Editable from main site
    """

    name        = models.CharField(max_length=100)
    style       = models.CharField(max_length=100, blank=True)
    recipe_url  = models.CharField(max_length=1024, blank=True)
    unreservable = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-id']
    
    def __unicode__(self):
        name = self.name
        brew_date = self.brew_date()
        
        if brew_date:
            name += " ({0})".format(brew_date)
            
        return name
    
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
        
    def brew_date(self):
        brewed = None
        
        for event in self.event_set.all():
            if event.event_type == 1:
                brewed = event.date
                break
        
        return brewed

    def is_gone(self):
        gone = False

        for event in self.event_set.all():
            if event.event_type == 6:
                gone = True
                break

        return gone

    def is_reservable(self):
        # Assumes all reservations are for 1 gallon
        # and that we only release 3 gallons of a particular beer
        return not self.is_gone() and self.reservation_set.count() < 3 and not self.unreservable


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
        (6, 'Gone'),
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


class Reservation(models.Model):
    """
    Reservation of a growler of beer for a user
    """
    
    beer = models.ForeignKey(Beer)
    user = models.ForeignKey(User)
    approved = models.BooleanField(default=False)
    fulfilled = models.BooleanField(default=False)
    
    def __unicode__(self):
        return unicode(self.beer) + " for " + self.user.username


# Signals - probably should be in a separate file but that feels like a waste
@receiver(pre_save, sender=Reservation)
def notify_reservation_user(sender, instance, **kwargs):
    # If the user has no email address, skip this
    try:
        original = Reservation.objects.get(pk=instance.id)
    except:
        original = None

    if original and instance.user.email:
        if not original.approved and instance.approved:
            msg = render_to_string('brewhouse/email/reservation_approved.html', {'reservation': instance})
            send_mail('Your beer reservation has been approved!', msg, 'home@nickpegg.com', [instance.user.email], fail_silently=True)
        if not original.fulfilled and instance.fulfilled:
            msg = render_to_string('brewhouse/email/reservation_fulfilled.html', {'reservation': instance})
            send_mail('Your beer reservation has been fulfilled!', msg, 'home@nickpegg.com', [instance.user.email], fail_silently=True)
