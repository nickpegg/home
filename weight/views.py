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
    else:
        callback = ''

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
        messages.success(request, "Your Withings account has been disconnected")
    except:
        messages.error(request, "Unable to disconnect Withings account")

    return redirect('weight-dashboard')
