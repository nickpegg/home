import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib import messages

import util
from models import Beer, Event, Tap, Reservation
from forms import AddBeerForm
from tasks import tweet_event


def display(request):
    taps = Tap.objects.all().order_by('number')

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

    # Gather up 10 beers and their brewed/ready events
    history = []
    for brewed_event in Event.objects.filter(event_type=1).order_by('-date')[:10]:
        beer = brewed_event.beer
        try:
            ready_event = beer.event_set.get(event_type=0)
        except:
            ready_event = None

        history.append((beer, brewed_event, ready_event))

    user_can_request = request.user.has_perm('brewhouse.add_reservation')

    return render(request, 'brewhouse/index.html', locals())


def history(request):
    # Gather up beers and their brewed/ready events
    history = []
    for brewed_event in Event.objects.filter(event_type=1).order_by('-date'):
        beer = brewed_event.beer
        try:
            ready_event = beer.event_set.get(event_type=0)
        except:
            ready_event = None

        history.append((beer, brewed_event, ready_event))

    return render(request, 'brewhouse/history.html', locals())


def beer_show(request, id):
    today = datetime.datetime.now().date()

    beer = get_object_or_404(Beer, pk=id)
    events = beer.event_set.filter(completed=True).filter(date__lte=today).order_by('date')
    future_events = beer.event_set.filter(completed=False).order_by('date')

    can_reserve = beer.is_reservable() and request.user.has_perm('brewhouse.add_reservation')
    beer_gone = beer.current_state() == 6

    return render(request, 'brewhouse/view_beer.html', locals())


@login_required
def beer_new(request):
    if not request.user.is_superuser:
        return redirect('brewhouse-display')

    if request.method == 'POST':
        form = AddBeerForm(request.POST)
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
                (7, 0),     # brewing
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

            return redirect('beer-show', b.id)
        else:
            pass    # TODO set an error
    else:
        form = AddBeerForm()

    return render(request, 'brewhouse/new_beer.html', locals())


@user_passes_test(lambda u: u.is_staff)
def beer_gone(request, beer_id):
    beer = get_object_or_404(Beer, pk=beer_id)

    if beer.current_state() == 6:
        messages.error(request, "This beer is already marked as 'gone'!")
        return redirect('beer-show', beer.id)

    # Create a new event marking this beer as gone
    event = Event()
    event.beer = beer
    event.date = datetime.datetime.now().date()
    event.event_type = 6    # Hard-coding this is kind of gross...
    event.completed = True
    event.save()

    tweet_event.delay(event)

    return redirect('beer-show', beer.id)


@login_required
def event_complete(request, event_id):
    if not request.user.is_superuser:
        return redirect('brewhouse-display')

    event = get_object_or_404(Event, pk=event_id)
    event.completed = True
    event.date = datetime.datetime.now().date()
    event.save()

    tweet_event.delay(event)

    return redirect('beer-show', event.beer.id)


@login_required
def new_reservation(request, beer_id):
    beer = get_object_or_404(Beer, pk=beer_id)

    if not request.user.has_perm('brewhouse.add_reservation'):
        messages.warning(request, "You're not allowed to reserve beer.")
        return redirect('beer-show', beer_id)

    if not beer.is_reservable():
        messages.warning(request, "That beer is not reservable!")
        return redirect('beer-show', beer_id)

    if Reservation.objects.filter(user=request.user, beer=beer):
        # User has already reserved this beer!
        messages.error(request, "You've already reserved a growler of this beer!")
        return redirect('beer-show', beer_id)

    if request.method == "POST" and request.POST.get('doit'):
        r = Reservation()
        r.beer = beer
        r.user = request.user
        r.save()

        messages.success(request, "Your beer reservation request has been made and is pending approval.")
        return redirect('beer-show', beer_id)

    return render(request, 'brewhouse/new_reservation.html', locals())


@login_required
def list_reservations(request):
    if not request.user.has_perm('brewhouse.add_reservation'):
        return redirect('brewhouse-display')

    reservations = request.user.reservation_set.all()
    return render(request, 'brewhouse/reservations.html', locals())


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    if request.user != reservation.user and not request.user.is_staff:
        messages.warning(request, "You cannot delete that reservation!")
    else:
        reservation.delete()
        messages.success(request, "Reservation removed")

    return redirect('brewhouse.views.list_reservations')
