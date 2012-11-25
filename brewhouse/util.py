import datetime

from models import Beer, Event


def beers_by_brew_date():
    """
    Returns a list of beers sorted by brewed date, oldest to newest
    """
    
    beers = []
    
    events = Event.objects.filter(event_type=1).filter(date__lte=datetime.datetime.now().date()).order_by('-date')
    for event in events:
        if event.beer not in beers:
            beers.append(event.beer)
        
    return beers

    
def not_done_beers():
    """
    Returns all of the beers which have any non-future events that also 
    do not have 'ready' events
    """
    
    beers = []
    
    for beer in beers_by_brew_date():
        if beer.is_started() and not beer.is_ready():
            beers.append(beer)
            
    # We want oldest first
    beers.reverse()
            
    return beers
    
def resolve_event_type(etype):
    """
    Takes an event type number and returns the text value for it
    """
    
    for a_type, desc in Event.TYPES:
        if a_type == etype:
            return desc
            
    return None

