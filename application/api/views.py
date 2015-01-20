from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from resto.models import Restaurant
from resto.views.account import *

def index(request):
    context = RequestContext(request)
    return render_to_response('restaurant.html', context)

