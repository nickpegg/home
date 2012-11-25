from django.conf.urls import patterns, url

urlpatterns = patterns('brewhouse.views',
    url(r'^$', 'display', name='brewhouse-display'),

    url(r'^beer/new/$', 'beer_new', name='beer-new'),
    url(r'^beer/(?P<id>\d+)/$', 'beer_show', name='beer-show'),
    url(r'^beer/(?P<id>\d+)/edit/$', 'beer_edit', name='beer-edit'),
    url(r'^beer/(?P<id>\d+)/delete/$', 'beer_delete', name='beer-delete'),
)
