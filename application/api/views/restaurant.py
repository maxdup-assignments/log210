from api.models import Restaurant, User, UserProfile
from api.serializers import RestaurantSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# plan to delete
from django.http import HttpResponse,  HttpResponseForbidden
from rest_framework.renderers import JSONRenderer
import json

@api_view(['GET','POST','PUT','DELETE'])
def resto(request, pk=None):

    if pk:
        resto = Restaurant.objects.get(pk=pk)

    if request.method == 'GET':

        # returns a single resto
        if pk:
            output = RestaurantSerializer(resto)

        #returns restos correspondiong to user
        elif 'user' in request.GET:
            user = User.objects.get(pk=request.GET['user'])
            restos = Restaurant.objects.filter(user=user)
            output = RestaurantSerializer(restos, many=True)

        # returns all restos
        else:
            restos = Restaurant.objects.all()
            output = RestaurantSerializer(restos, many=True)

        return Response(output.data)

    elif request.method == 'POST':

        # creates a resto
        resto = RestaurantSerializer(data=request.data)
        if resto.is_valid():
            resto.save()
            return Response(resto.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(resto.errors,
                            resto=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT' and pk:

        # updates a resto
        request.data.pop('user')

        if 'new_user' in request.data:
            if request.data['new_user']['value']:
                new_user = User.objects.get(
                    pk=request.data['new_user']['value'])
                resto.user = new_user
            else:
                resto.user = None
            resto.save()

        resto = RestaurantSerializer(resto, data=request.data, partial=True)
        if resto.is_valid():
            resto.save()
            return Response(resto.data)
        return Response(resto.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':

        # deletes a resto
        resto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def populate_resto(request):
    # a script that populates the database with restaurants

    restaurateurs = UserProfile.objects.filter(is_restaurateur=True)

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

