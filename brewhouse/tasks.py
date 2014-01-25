import logging

import celery
from twitter import Twitter, OAuth

from home import settings


@celery.task
def tweet_event(event):
    messages = {
        0: "{0} is carbonated and ready for drinking! Woohoo!",
        1: "{0} is done brewing!",
        2: "{0} is now in primary fermentation. Time for 1 billion of my single-celled friends to get to work!",
        3: "{0} is now in secondary fermenatation.",
        4: "{0} has been kegged.",
        6: "The keg's been kicked! {0} is all gone. :(",
        7: "Brew day! In the kettle: {0}",
    }

    if event.event_type not in messages.keys():
        logging.warning("Tried to tweet an event that I don't have a message for")
        return None
    else:
        message = messages[event.event_type].format(event.beer.name)

    if event.event_type == 7 and event.beer.recipe_url:
        message += ", recipe: " + event.beer.recipe_url

    # Connect up to Twitter
    api = Twitter(auth=OAuth(settings.BREWERY_TWITTER_ACCESS_TOKEN,
                             settings.BREWERY_TWITTER_ACCESS_SECRET,
                             settings.BREWERY_TWITTER_CONSUMER_KEY,
                             settings.BREWERY_TWITTER_CONSUMER_SECRET))

    ret = api.statuses.update(status=message)
    logging.info("Posted to Twitter (tweet id {0}): {1}".format(ret.get(id), message))
