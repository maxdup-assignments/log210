from django.http import HttpResponse,  HttpResponseForbidden

from api.models import Restaurant, User, UserProfile

from api.serializers import RestaurantSerializer
from rest_framework.renderers import JSONRenderer
import json

def create_resto(request):
    # creates a restorant in database.
    # returns the created restaurant.
    
    restoinfo = json.loads(request.body)
    if (restoinfo['user']):
        restaurateur = User.objects.get(pk=restoinfo['user'])
        resto = Restaurant.objects.create(user=restaurateur,
                                          name=restoinfo['name'],
                                          menu=restoinfo['menu'],
                                          address=restoinfo['address'])
    else:
        resto = Restaurant.objects.create(name=restoinfo['name'],
                                          menu=restoinfo['menu'],
                                          address=restoinfo['address'])
    resto.save()
    resto = RestaurantSerializer(resto)
    return HttpResponse(JSONRenderer().render(resto.data))

def delete_resto(request):
    # deletes a restaurant in database
        
    restoinfo = json.loads(request.body)
    resto = Restaurant.objects.get(pk=restoinfo['pk'])
    resto.delete()
    return HttpResponse({'success': True})

def edit_resto(request):
    # updates a restaurant
    # -receives a json formated restaurant 
    # -returns the updated restaurant

    restoinfo = json.loads(request.body)
    resto = Restaurant.objects.get(pk=restoinfo['pk'])
    print(restoinfo)
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

def assigned_resto(request):
    # returns all restaurants assigned to the current user in an array

    print request.user.pk
    user = User.objects.get(pk=request.user.pk)
    restos = Restaurant.objects.filter(user=user)

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

    restaurateurs = UserProfile.objects.filter(is_restaurateur=True)
    print restaurateurs

    if not Restaurant.objects.filter(name='Pataterie').exists():
        resto = Restaurant.objects.create(
            name='Pataterie',
            address='1877 Rue Amherst',
            user=restaurateurs[1].user,
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
            address='2020 Rue University',
            user=restaurateurs[2].user,
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
            address='895 Rue de la Gauchetiere',
            user=restaurateurs[3].user,
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
            address='67 Rue de la Gauchetiere',
            user=None,
            menu={})
        resto.save()

    return HttpResponse({'success': True})

