import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

import util
from models import Beer, Event, Tap


def display(request):
    taps = Tap.objects.all()
    
    # Gather up the upcoming-but-not-ready beers
    beers = []
    for beer in util.not_done_beers():
        try:
            ready = beer.event_set.get(event_type=0).date
        except:
            ready = 'Unknown'

        try:            
            brewed_on = beer.event_set.get(event_type=1).date
        except:
            brewed_on = 'Unknown'
            
        beers.append((beer, util.resolve_event_type(beer.current_state()), brewed_on, ready))
        
    
    return render(request, 'brewhouse/index.html', locals())
    
    
def beer_show(request, id):
    today = datetime.datetime.now().date()

    beer = get_object_or_404(Beer, pk=id)
    events = beer.event_set.filter(date__lte=today).order_by('date')
    future_events = beer.event_set.filter(date__gt=today).order_by('date')
    
    return render(request, 'brewhouse/view_beer.html', locals())
    

@login_required
def beer_new(request):
    if not request.user.is_superuser:
        redirect('display')
        
    if request.method == 'POST':
        form = NewBeerForm(request.POST)
        if form.is_valid():
            b = Beer()
            b.name = form.cleaned_data['name']
            b.style = form.cleaned_data['style']
            b.recipe_url = form.cleaned_data['recipe_url']
            b.save()
            
            # Create some basic events based on the brewed-on date
            # tuple is of (event_type, days_since_brew_date)
            brew_date = form.cleaned_data['brew_date']

            events = (
                (1, 0),     # brewed
                (2, 0),     # primary fermentation
                (3, 7),     # secondary fermentation
                (4, 21),    # kegged
                (0, 28),    # ready!
            )
            
            for etype, num_days in events:
                event = Event()
                event.beer = b
                event.event_type = etype
                event.date = brew_date + datetime.timedelta(days=num_days)
                event.save()
        else:
            pass    # TODO set an error
    else:
        form = NewBeerForm(request.POST)
        
    return render(request, 'new_beer.html', locals())
    
    
@login_required
def beer_edit(request, id):
    if not request.user.is_superuser:
        redirect('display')
        
    beer = get_object_or_404(pk=id)
    if request.method == 'POST':
        form = BeerForm(request.POST, instance=beer)
        
        if form.is_valid():
            beer = form.save()
        else:
            pass    #TODO set an error
        
    else:
        form = BeerForm(instance=beer)

@login_required    
def beer_delete(request, id):
    return HttpResponse("Not implemented.")
    if not request.user.is_superuser:
        redirect('display')

