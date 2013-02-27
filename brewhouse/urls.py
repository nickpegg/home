from django.conf.urls import patterns, url

urlpatterns = patterns('brewhouse.views',
    url(r'^$', 'display', name='brewhouse-display'),
    
    url(r'^history/$', 'history', name='brewhouse-history'),

    url(r'^beer/new/$', 'beer_new', name='beer-new'),
    url(r'^beer/(?P<id>\d+)/$', 'beer_show', name='beer-show'),
    url(r'^beer/(?P<id>\d+)/edit/$', 'beer_edit', name='beer-edit'),
    url(r'^beer/(?P<id>\d+)/delete/$', 'beer_delete', name='beer-delete'),
    url(r'^beer/(?P<beer_id>\d+)/gone/$', 'beer_gone'),
    url(r'^beer/(?P<beer_id>\d+)/reserve/$', 'new_reservation'),

    url(r'^event/(?P<event_id>\d+)/done/$', 'event_complete', name='event-complete'),
    
    url(r'^reservations/$', 'list_reservations'),
    
)
