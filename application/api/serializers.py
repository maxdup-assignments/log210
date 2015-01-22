from rest_framework import serializers
from api.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    pk = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name',
                  'last_name', 'is_superuser', 'is_staff')

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    pk = serializers.CharField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ('pk', 'user', 'adresse', 'telephone', 'date_naissance')
        depth = 1

class Restaurant(serializers.ModelSerializer):
    user = UserSerializer()
    pk = serializers.CharField(read_only=True)
    class Meta:
        model = Restaurant
        fields = ('pk', 'user', 'name', 'menu')
