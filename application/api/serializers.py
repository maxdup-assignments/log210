from rest_framework import serializers
from api.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    pk = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('pk','password', 'username', 'email', 'first_name', 'last_name')

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    pk = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        depth = 1
        fields = ('pk', 'user', 'adresse', 'telephone', 'date_naissance',
                  'is_restaurateur', 'is_entrepreneur',
                  'is_livreur', 'is_admin')

    def create(self, data):
        user = User(
            email=data['user']['email'],
            username=data['user']['email'],
            last_name=data['user']['last_name'],
            first_name=data['user']['first_name'])
        user.set_password(data['user']['password'])
        user.save()

        profile = UserProfile(
            user=user,
            adresse=data['adresse'],
            telephone=data['telephone'],
            date_naissance=data['date_naissance'],
            is_restaurateur=data['is_restaurateur'])
        profile.save()

        return profile

class RestaurantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    pk = serializers.CharField(read_only=True)

    class Meta:
        model = Restaurant
        fields = ('pk', 'user', 'name', 'menu', 'address')

class CommandeSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()
    pk = serializers.CharField(read_only=True)

    class Meta:
        model = Commande
        fields = ('pk', 'restaurant', 'details', 'status')
