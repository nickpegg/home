import datetime

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
    
    name        = forms.CharField(max_length=100)
    style       = forms.CharField(max_length=100, required=False)
    recipe_url  = forms.CharField(max_length=1024, required=False)

    brew_date   = forms.DateField(initial=datetime.datetime.now().date())
