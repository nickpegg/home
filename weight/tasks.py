import calendar
import logging

import celery
import withings

from home import settings
from models import WeightEntry, WithingsAuth


KG_TO_LBS = 2.20462


@celery.task
def fetch_weight(user):
    """
    Error codes:
    0   Success
    1   User needs to connect their Withings account
    """

    try:
        wauth = user.withings_auth
    except:
        logging.warning("Given user needs to connect to their Withings account")
        return 1

    creds = withings.WithingsCredentials(
        consumer_key=settings.WITHINGS_CONSUMER_KEY,
        consumer_secret=settings.WITHINGS_CONSUMER_SECRET,
        access_token=wauth.oauth_token,
        access_token_secret=wauth.oauth_secret,
        user_id=wauth.uid)
    api = withings.WithingsApi(creds)
    logging.info("Logged in to API.")

    entries = WeightEntry.objects.filter(user=user).order_by('-when')

    if entries:
        startdate = calendar.timegm(entries[0].when.utctimetuple()) + 1
        logging.info("Using a start timestamp of " + str(startdate))
        measurements = api.get_measures(meastype=1, startdate=startdate)
    else:
        measurements = api.get_measures(meastype=1)

    logging.info("Grabbed measurements, adding to DB")
    if len(measurements) == 0:
        logging.info("Didn't grab shit, check the startdate?")

    for measurement in measurements:
        if not measurement.is_measure():
            continue

        logging.info("Daters: " + str(measurement.data))

        entry = WeightEntry()
        entry.user = user
        entry.when = measurement.date
        entry.weight = measurement.weight * KG_TO_LBS
        entry.source = 1
        entry.save()

    return 0


@celery.task
def update_all_users():
    """
    Periodic task which iterates through users and pulls their latest data
    """

    for wa in WithingsAuth.objects.all():
        fetch_weight.apply_async([wa.user], ignore_result=True)

    return 0
