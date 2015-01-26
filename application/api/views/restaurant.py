from django.http import HttpResponse,  HttpResponseForbidden

from api.models import Restaurant, User

from api.serializers import RestaurantSerializer
from rest_framework.renderers import JSONRenderer
import json

def create_resto(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    
    restoinfo = json.loads(request.body)
    restaurateur = User.objects.get(pk=restoinfo['restaurateur'])
    resto = Restaurant.objects.create(user=restaurateur,
                                      name=restoinfo['name'],
                                      menu=restoinfo['menu'])
    resto.save()
    return HttpResponse(json.loads(request.body))

def delete_resto(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
        
    restoinfo = json.loads(request.body)
    resto = Restaurant.objects.get(pk=restoinfo['pk'])
    resto.delete()
    return HttpResponse({'success': True})


def all_resto(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    restos = Restaurant.objects.all()
    response = []
    for resto in restos:
        resto = RestaurantSerializer(resto)
        response.append(resto.data)
    return HttpResponse(JSONRenderer().render(response))
    
