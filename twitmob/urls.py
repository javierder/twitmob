from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
    url(r'^crowds/$', 'main.views.campaigns', name='crowds'),
    url(r'^crowd/new/$', 'main.views.new_campaign', name='new_crowd'),
     url(r'^what-is-mycrowder/$', direct_to_template, {
        'template': 'whatisthis.html'
    }),
  
    url(r'^crowd/edit/(?P<id>\d+)/$', 'main.views.edit_campaign', name='edit_campaign'),


    url(r'^crowds/mine/$', 'main.views.my_crowds', name='my_crowds'),
    url(r'^crowd/join/(?P<id>\d+)/$', 'main.views.join_campaign', name='join_campaign'),
    url(r'^c/(?P<id>\d+)/$', 'main.views.redirect_crowd', name='redirect_crowd'),
    url(r'^crowd/join/(?P<id>\d+)/(?P<slug>[-\w]+)/$', 'main.views.join_campaign', name='join_campaign'),
    url(r'^crowd/leave/$', 'main.views.leave_campaign', name='leave_campaign'),
    url(r'^campaigns/new_message/$', 'main.views.new_message', name='new_message'),
    # url(r'^campaigns/edit_message/$', 'main.views.edit_message', name='edit_message'),
    url(r'^campaigns/delete_message/$', 'main.views.delete_message', name='delete_message'),
    url(r'^login/$', 'main.views.force_login', name='force_login'),
    url(r'^logout/$', 'main.views.force_logout', name='logout'),



	url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="auth_login"),

    (r'^twitter/', include('twython_django_oauth.urls')),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
