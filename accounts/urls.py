from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('social_auth.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/', 'template_name': 'accounts/logout.html'}),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    
    url(r'^password/change/$', 'django.contrib.auth.views.password_change', 
        {'template_name': 'accounts/pwd_change.html', 'post_change_redirect': '/accounts/profile'}),

    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset', 
        {
            'template_name': 'accounts/pwd_reset.html',
            'email_template_name': 'accounts/email/password_reset.html',
            'subject_template_name': 'accounts/email/password_reset_subject.txt',
        }),
    url(r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done', 
        {'template_name': 'accounts/pwd_reset_done.html'}),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'accounts/pwd_reset_confirm.html'}),
    url(r'^password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'accounts/pwd_reset_complete.html'}),
    
    url(r'^signup/$', 'accounts.views.register'),
    url(r'^profile/$', 'accounts.views.profile'),
    url(r'^delete/$', 'accounts.views.delete'),
)
