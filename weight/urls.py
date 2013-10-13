from django.conf.urls import patterns, url

urlpatterns = patterns('weight.views',
    url(r'^$', 'dashboard', name='weight-dashboard'),
    url(r'^new/$', 'new'),

    url(r'^connect/withings/$', 'connect_withings'),
    url(r'^connect/withings/authorize/$', 'connect_withings_finish'),

    url(r'^disconnect/withings/$', 'disconnect_withings'),

    # Temporary testing crap
    url(r'update/$', 'update'),
    url(r'update/all/$', 'update_all'),
)
