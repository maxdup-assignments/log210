from django.shortcuts import render_to_response
from django.template import RequestContext

from api.views.account import *
from api.views.restaurant import *
from api.views.commande import *

def index(request):
    context = RequestContext(request)
    return render_to_response('restaurant.html', context)

