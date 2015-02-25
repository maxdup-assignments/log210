from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import DictField, ListField

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    date_naissance = models.CharField(max_length=128)
    adresse = ListField()
    telephone = models.CharField(max_length=15)

class Restaurant(models.Model):
    user = models.OneToOneField(User, null=True)
    name = models.CharField(max_length=80)
    menu = DictField()

class Commande(models.Model):
    user = models.OneToOneField(User)
    restaurant = models.OneToOneField(Restaurant)
    details = DictField()
    status = models.CharField(max_length=10)
