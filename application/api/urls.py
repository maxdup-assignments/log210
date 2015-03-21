from django.conf.urls import patterns, url

from api.views.account import *
from api.views.restaurant import *
from api.views.commande import *
from api.data_population import populate_database

urlpatterns = patterns('',
    url(r'^login', user_login, name='login'),
    url(r'^logout', user_logout, name='logout'),

    url(r'^all_staff', get_staff, name='get_staff'),
    url(r'^all_profiles', get_profiles, name='get_profiles'),
    url(r'^register', register, name='register'),
    url(r'^edit_profile', edit_profile, name='edit_profile'),
    url(r'^delete_profile', delete_profile, name='delete_profile'),

    url(r'^populatedb', populate_database),

    url(r'^resto(?:/(?P<pk>\w+))?$', resto),
    url(r'^profile(?:/(?P<pk>\w+))?$', profile),
    url(r'^commande(?:/(?P<pk>\w+))?$', commande),
)
