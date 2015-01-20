from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from api.models import Restaurant
from api.views.account import *

from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    context = RequestContext(request)
    return render_to_response('restaurant.html', context)

