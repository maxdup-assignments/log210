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
    if (restoinfo['user']):
        restaurateur = User.objects.get(pk=restoinfo['user'])
        resto = Restaurant.objects.create(user=restaurateur,
                                          name=restoinfo['name'],
                                          menu=restoinfo['menu'])
    else:
        resto = Restaurant.objects.create(name=restoinfo['name'],
        menu=restoinfo['menu'])
    resto.save()
    resto = RestaurantSerializer(resto)
    return HttpResponse(JSONRenderer().render(resto.data))

def delete_resto(request):
    # deletes a restaurant in database
    if not request.user.is_superuser:
        return HttpResponseForbidden()
        
    restoinfo = json.loads(request.body)
    resto = Restaurant.objects.get(pk=restoinfo['pk'])
    resto.delete()
    return HttpResponse({'success': True})

def edit_resto(request):
    # updates a restaurant
    # -receives a json formated restaurant 
    # -returns the updated restaurant

    if request.method != 'POST' or not request.user.is_staff:
        return HttpResponseForbidden()

    restoinfo = json.loads(request.body)
    resto = Restaurant.objects.get(pk=restoinfo['pk'])

    del restoinfo['user']
    resto.__dict__.update(**restoinfo)
    if 'new_user' in restoinfo:
        if restoinfo['new_user']['value']:
            new_user = User.objects.get(pk=restoinfo['new_user']['value'])
            resto.user = new_user
        else:
            resto.user = None
    resto.save()
    resto = RestaurantSerializer(resto)
    return HttpResponse(JSONRenderer().render(resto.data))

def all_resto(request):
    # returns all restaurants in an array

    restos = Restaurant.objects.all()
    response = []
    for resto in restos:
        resto = RestaurantSerializer(resto)
        response.append(resto.data)
    return HttpResponse(JSONRenderer().render(response))

def edit_menu(request):
    # updates the menu of a restaurant
    # -receives a json formated restaurant 
    # -returns the updated restaurant

    restoinfo = json.loads(request.body)
    resto = Restaurant.objects.get(pk=restoinfo['pk'])

    for menu in restoinfo['menu']['sous_menus']:
        if 'newitem' in menu:
            del menu['newitem']
    resto.menu = restoinfo['menu']
    resto.save()
    response = RestaurantSerializer(resto)
    return HttpResponse(JSONRenderer().render(response.data))

    
def populate_resto(request):
    # a script that populates the database with restaurants

    restaurateurs = User.objects.filter(is_staff=True)
    len(restaurateurs)

    if not Restaurant.objects.filter(name='Pataterie').exists():
        resto = Restaurant.objects.create(
            name='Pataterie',
            user=restaurateurs[1],
            menu={
                'sous_menus': [
                    {'name': 'menu matin',
                     'items': [
                        {'name': 'patate',
                         'desc': 'des patates',
                         'price': '3'},
                        {'name': 'patate small',
                         'desc': 'des petites patates',
                         'price': '5'}
                    ]},
                    {'name': 'menu soir',
                     'items': [{
                         'name': 'poutine',
                         'desc': 'de la poutine',
                         'price': '7'},
                        {'name': 'hotdog',
                         'desc': 'des hotdogs',
                         'price': '6'},
                    ]}
                ]
            })
        resto.save()

    if not Restaurant.objects.filter(name='Subway').exists():
        resto = Restaurant.objects.create(
            name='Subway',
            user=restaurateurs[2],
            menu={
                'sous_menus': [
                    {'name': 'menu matin',
                     'items': [
                        {'name': 'sous-marin',
                         'desc': '12 pouces',
                         'price': '5'}
                    ]}
                ]
            })
        resto.save()

    if not Restaurant.objects.filter(name='McDonalds').exists():
        resto = Restaurant.objects.create(
            name='McDonalds',
            user=restaurateurs[3],
            menu={
                'sous_menus': [
                    {'name': 'eat fat',
                     'items': [
                        {'name': 'BigMac',
                         'desc': '100% boeuf',
                         'price': '7'}
                    ]}
                ]
            })
        resto.save()

    if not Restaurant.objects.filter(name='Buffet').exists():
        resto = Restaurant.objects.create(
            name='Buffet',
            user=None,
            menu={})
        resto.save()

    return HttpResponse({'success': True})

