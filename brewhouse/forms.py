from django import forms

from models import Beer, Event


class BeerForm(forms.Form):
    class Meta:
        model = Beer

class EventForm(forms.Form):
    class Meta:
        model = Event


class AddBeerForm(forms.Form):
    EVENT_TYPES = (
        (0, 'Ready'),
        (1, 'Brewed'),
        (2, 'Primary Fermentation'),
        (3, 'Secondary Fermentation'),
        (4, 'Kegged'),
        (5, 'Bottled'),
        (6, 'Ready'),
    )
    
    name        = models.CharField(max_length=100)
    style       = models.CharField(max_length=100)
    recipe_url  = models.CharField(max_length=1024)

    brew_date   = models.DateField(auto_now_add=True)
