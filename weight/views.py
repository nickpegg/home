from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib import messages
from django.core.urlresolvers import reverse

import withings

from home import settings

import tasks
from models import WithingsAuth, WeightEntry



@login_required
@permission_required('weight.can_use')
def dashboard(request):
    try:
        withings_auth = request.user.withings_auth
        connected = True
    except:
        connected = False

    weight = None
    if connected:
        entries = WeightEntry.objects.filter(user=request.user)
        if entries:
            current_weight = entries[0].weight

    return render(request, 'weight/index.html', locals())


@login_required
@permission_required('weight.can_use')
def update(request):
    #result = tasks.fetch_weight.delay(request.user)
    result = tasks.fetch_weight.delay(request.user)
    err_code = result.get(timeout=15)

    if err_code == 1:
        messages.error(request, "You need to connect your Withings account first!")
    else:
        messages.success(request, "Your weight data has been updated")

    return redirect('weight-dashboard')


@login_required
def update_all(request):
    # TODO Remove this view and make this a periodic task
    tasks.update_all_users.delay()

    return redirect('weight-dashboard')


@login_required
@permission_required('weight.can_use')
def new(request):
    raise NotImplementedError()


@login_required
@permission_required('weight.can_use')
def connect_withings(request):
    default_callback = 'https://www.home.nickpegg.com' + reverse('weight.views.connect_withings_finish')

    if not settings.DEBUG:
        callback = default_callback
    elif 'callback_url' in request.GET:
        callback = request.GET['callback_url']
        request.session['withings_callback_url'] = callback
    else:
        callback = ''
        if 'withings_callback_url' in request.session:
            default_callback = request.session['withings_callback_url']

    if callback:
        auth = withings.WithingsAuth(settings.WITHINGS_CONSUMER_KEY, settings.WITHINGS_CONSUMER_SECRET)
        auth_url = auth.get_authorize_url(callback_url=callback)

        # Stash the request token info for later use
        request.session['withings_auth'] = auth

        return redirect(auth_url)
    else:
        return render(request, 'weight/connect/withings.html', locals())


@login_required
@permission_required('weigh.can_use')
def connect_withings_finish(request):
    if 'oauth_verifier' in request.GET:
        auth = request.session['withings_auth']
        creds = auth.get_credentials(request.GET['oauth_verifier'])
        del request.session['withings_auth']

        # Stash the creds
        wa = WithingsAuth()
        wa.user = request.user
        wa.uid = creds.user_id
        wa.oauth_token = creds.access_token
        wa.oauth_secret = creds.access_token_secret
        wa.save()

        # Snag all of their data while you're at it
        request.session['withings_data_pending'] = True
        tasks.fetch_weight.delay(request.user)

        messages.success(request, 'You have successfully connected your Withings account')
    elif settings.DEBUG:
        return render(request, 'weight/connect/withings_authorize.html', locals())

    return redirect('weight-dashboard')


@login_required
@permission_required('weight.can_use')
def disconnect_withings(request):
    try:
        wa = request.user.withings_auth
        wa.delete()

        WeightEntry.objects \
            .filter(user=request.user) \
            .filter(source=WeightEntry.SOURCE_WITHINGS) \
            .delete()

        messages.success(request, "Your Withings account has been disconnected")
    except:
        messages.error(request, "Unable to disconnect Withings account")

    return redirect('weight-dashboard')


@login_required
@permission_required('weight.can_use')
def subscribe_withings(request):
    subscription_url = request.GET.get('callback_url')
    if not subscription_url:
        if settings.DEBUG:
            subscription_url = request.session.get('withings_callback_url')
            return render(request, 'weight/subscribe/withings.html', locals())
        else:
            subscription_url = 'http://home.nickpegg.com' + reverse('weight.views.subscribe_withings_receive')

    tasks.subscribe_withings.delay(request.user, subscription_url)

    return redirect('weight-dashboard')


@login_required
@permission_required('weight.can_use')
def unsubscribe_withings(request):
    wauth = get_object_or_404(WithingsAuth, user=request.user)

    creds = withings.WithingsCredentials(
        consumer_key=settings.WITHINGS_CONSUMER_KEY,
        consumer_secret=settings.WITHINGS_CONSUMER_SECRET,
        access_token=wauth.oauth_token,
        access_token_secret=wauth.oauth_secret,
        user_id=wauth.uid)
    api = withings.WithingsApi(creds)

    url = request.session.get('withings_callback_url')
    if not url:
        url = 'http://home.nickpegg.com' + reverse('weight.views.subscribe_withings_receive')

    # TODO delay() this
    tasks.unsubscribe_withings.delay(request.user, url)

    # TODO fix debugs
    return HttpResponse(api.list_subscriptions())


def subscribe_withings_receive(request):
    """
    Handles data that Withings posts to us
    """

    if request.method == 'POST':
        wauth = get_object_or_404(WithingsAuth, uid=request.POST['userid'])

        tasks.fetch_weight.delay(wauth.user,
                                 startdate=request.POST['startdate'],
                                 enddate=request.POST['enddate'])

        return HttpResponse("Thanks for the data, Withings! <3")
    else:
        return HttpResponse("Hi Withings! Gimme your datas!")
