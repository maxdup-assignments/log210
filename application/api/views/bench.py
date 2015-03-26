from api.views import account
from api.views import restaurant
from api.views import commande as order

from pycallgraph import PyCallGraph, Config, GlobbingFilter
from pycallgraph.output import GraphvizOutput


config = Config(max_depth=6)
config.trace_filter = GlobbingFilter(exclude=[
    'pycallgraph.*',
    'rest_framework.views.*',
    'rest_framework.decorators.*',
    'rest_framework.request.*',
    'rest_framework.negotiation.*',
    'rest_framework.permissions.*',
    'django.conf.*',
    'django.views.*',
    'django.utils.*',
    'django.middleware.*',
    'django.template.*',
    'django.http.*',
])

def profile(request, pk=None):
    output_file='../doc/account_'+request.method+'.png'
    output = GraphvizOutput(output_file=output_file)
    config.max_depth = 7
    with PyCallGraph(output=output, config=config):
        output = account.profile(request, pk)
        return output

def resto(request, pk=None):
    output_file='../doc/resto_'+request.method+'.png'
    output = GraphvizOutput(output_file=output_file)
    config.max_depth = 6
    with PyCallGraph(output=output, config=config):
        output = restaurant.resto(request, pk)
        return output

def commande(request, pk=None):
    output_file='../doc/commande_'+request.method+'.png'
    output = GraphvizOutput(output_file=output_file)
    config.max_depth = 6
    with PyCallGraph(output=output, config=config):
        output = order.commande(request, pk)
        return output
