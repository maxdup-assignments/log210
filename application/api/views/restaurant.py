from api.models import Restaurant, User, UserProfile
from api.serializers import RestaurantSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET','POST','PUT','DELETE'])
def resto(request, pk=None):

    if pk:
        resto = Restaurant.objects.get(pk=pk)

    if request.method == 'GET':

        # returns a single resto
        if pk:
            output = RestaurantSerializer(resto)

        # returns restos correspondiong to user
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
        user = None
        if request.data['user']:
            user = User.objects.get(pk=request.data['user'])
        resto = Restaurant(
            user=user,
            name=request.data['name'],
            address=request.data['address'],
            menu={},
        )
        resto.save()
        resto = RestaurantSerializer(resto)
        return Response(resto.data,
                        status=status.HTTP_201_CREATED)

    elif request.method == 'PUT' and pk:

        # updates a resto
        if 'user' in request.data:
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
