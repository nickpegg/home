from django.conf.urls import patterns, url, include
from tastypie.api import Api

import api


v1_api = Api(api_name='v1')
v1_api.register(api.TapResource())
v1_api.register(api.BeerResource())
v1_api.register(api.UpcomingResource())

urlpatterns = patterns('brewhouse.views',
    url(r'^$', 'display', name='brewhouse-display'),

    url(r'^history/$', 'history', name='brewhouse-history'),

    url(r'^beer/new/$', 'beer_new', name='beer-new'),
    url(r'^beer/(?P<id>\d+)/$', 'beer_show', name='beer-show'),
    url(r'^beer/(?P<beer_id>\d+)/gone/$', 'beer_gone'),

    url(r'^beer/(?P<beer_id>\d+)/reserve/$', 'new_reservation'),

    url(r'^event/(?P<event_id>\d+)/done/$', 'event_complete', name='event-complete'),

    url(r'^reservations/$', 'list_reservations'),
    url(r'^reservations/(?P<reservation_id>\d+)/delete/$', 'delete_reservation'),

    # API shiz
    url(r'^api/', include(v1_api.urls)),
)
