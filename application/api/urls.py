from django.conf.urls import patterns, url

from api.views.account import *
from api.views.restaurant import *
from api.views.commande import *

urlpatterns = patterns('',
    url(r'^register', register, name='register'),
    url(r'^login', user_login, name='login'),
    url(r'^logout', user_logout, name='logout'),
    url(r'^all_staff', get_staff, name='get_staff'),
    url(r'^profile', get_current_profile, name='get_current_profile'),
    url(r'^all_profiles', get_profiles, name='get_profiles'),
    url(r'^edit_profile', edit_profile, name='edit_profile'),
    url(r'^delete_profile', delete_profile, name='delete_profile'),
    url(r'^populateuser', populateUser, name='populateUser'),

    url(r'^create_resto', create_resto, name='create_resto'),
    url(r'^delete_resto', delete_resto, name='delete_resto'),
    url(r'^edit_resto', edit_resto, name='edit_resto'),
    url(r'^all_resto', all_resto, name='all_resto'),
    url(r'^assigned_resto', assigned_resto, name='assigned_resto'),
    url(r'^populateresto', populate_resto, name='populateresto'),
    url(r'^create_commande', create_commande, name='create_commande'),
    url(r'^get_commande', get_commande, name='get_commande'),
    url(r'^resto_commande', resto_commande, name='resto_commande'),
    url(r'^update_commande', update_commande_status, name='update_commande_status'),
    url(r'^populatecommande', populate_commande, name='populatecommandes'),
    url(r'^resto(?:/(?P<pk>\w+))?$', resto),
    url(r'^profile(?:/(?P<pk>\w+))?$', profile),
)
