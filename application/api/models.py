from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import DictField, ListField

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    date_naissance = models.CharField(max_length=128)
    adresse = ListField()
    telephone = models.CharField(max_length=15)
    is_admin = models.BooleanField(default=False)
    is_entrepreneur = models.BooleanField(default=False)
    is_restaurateur = models.BooleanField(default=False)
    is_livreur = models.BooleanField(default=False)

class Restaurant(models.Model):
    user = models.OneToOneField(User, null=True)
    name = models.CharField(max_length=80)
    menu = DictField()
    address = models.CharField(max_length=80)

class Commande(models.Model):
    restaurant = models.OneToOneField(Restaurant, null=True, blank=True)
    details = DictField()
    status = models.CharField(max_length=10)
