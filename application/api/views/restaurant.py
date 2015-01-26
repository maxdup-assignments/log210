from django.http import HttpResponse,  HttpResponseForbidden

from api.models import Restaurant, User

from api.serializers import RestaurantSerializer
from rest_framework.renderers import JSONRenderer
import json

def create_resto(request):
    # creates a restorant in database.
    # returns the created restaurant.
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    
    restoinfo = json.loads(request.body)
    restaurateur = User.objects.get(pk=restoinfo['user'])
    resto = Restaurant.objects.create(user=restaurateur,
                                      name=restoinfo['name'],
                                      menu=restoinfo['menu'])
    resto.save()
    resto = RestaurantSerializer(resto)
    return HttpResponse(JSONRenderer().render(resto.data))

def delete_resto(request):
    #deletes a restaurant in database
    if not request.user.is_superuser:
        return HttpResponseForbidden()
        
    restoinfo = json.loads(request.body)
    resto = Restaurant.objects.get(pk=restoinfo['pk'])
    resto.delete()
    return HttpResponse({'success': True})

def edit_resto(request):
    if request.method == 'POST':
        restoinfo = json.loads(request.body)
        del restoinfo['user']

        resto = Restaurant.objects.get(pk=restoinfo['pk'])
        resto.__dict__.update(**restoinfo)

        if 'new_user' in restoinfo:
            new_user = User.objects.get(pk=restoinfo.new_user.value)
            resto.user = new_user
        resto.save()
    return HttpResponse({'success':True})

def all_resto(request):
    # returns all restaurants in an array
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    restos = Restaurant.objects.all()
    response = []
    for resto in restos:
        resto = RestaurantSerializer(resto)
        response.append(resto.data)
    return HttpResponse(JSONRenderer().render(response))
    
