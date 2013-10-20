from django.conf.urls import patterns, url

urlpatterns = patterns('weight.views',
    url(r'^$', 'dashboard', name='weight-dashboard'),
    url(r'^new/$', 'new'),

    url(r'^(?P<days>\d+)/days/$', 'n_days'),

    url(r'^connect/withings/$', 'connect_withings'),
    url(r'^connect/withings/authorize/$', 'connect_withings_finish'),

    url(r'^disconnect/withings/$', 'disconnect_withings'),

    url(r'^subscribe/withings/$', 'subscribe_withings'),
    url(r'^unsubscribe/withings/$', 'unsubscribe_withings'),
    url(r'^subscribe/withings/receive/$', 'subscribe_withings_receive'),

    url(r'^highcharts/(?P<days>\d+)/days/$', 'highcharts_n_days'),

    # Temporary testing crap
    url(r'update/$', 'update'),
    url(r'update/all/$', 'update_all'),
)
