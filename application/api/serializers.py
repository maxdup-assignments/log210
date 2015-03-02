from rest_framework import serializers
from api.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    pk = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name')

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    pk = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('pk', 'user', 'adresse', 'telephone', 'date_naissance',
                  'is_admin', 'is_restaurateur', 'is_entrepreneur', 'is_livreur')
        depth = 1

class RestaurantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    pk = serializers.CharField(read_only=True)
    class Meta:
        model = Restaurant
        fields = ('pk', 'user', 'name', 'menu', 'address')

class CommandeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    restaurant = RestaurantSerializer()
    pk = serializers.CharField(read_only=True)
    class Meta:
        model = Commande
        fields = ('pk', 'user', 'restaurant', 'details', 'status')
