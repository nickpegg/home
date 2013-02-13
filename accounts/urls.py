from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('social_auth.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/', 'template_name': 'accounts/logout.html'}),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    
    url(r'^profile/$', 'accounts.views.profile'),
)
