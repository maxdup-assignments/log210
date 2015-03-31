from django.conf.urls import patterns, url

from api.views.account import *
from api.views.restaurant import resto
from api.views.commande import commande
from api.data_population import populate_database
from api.views.bench import *


urlpatterns = patterns('',
    url(r'^login', user_login, name='login'),
    url(r'^logout', user_logout, name='logout'),

    url(r'^resto(?:/(?P<pk>\w+))?$', resto),
    url(r'^profile(?:/(?P<pk>\w+))?$', profile),
    url(r'^commande(?:/(?P<pk>\w+))?$', commande),

    url(r'^populatedb', populate_database),
)
