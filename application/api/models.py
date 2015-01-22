from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import DictField

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    date_naissance = models.CharField(max_length=128)
    adresse = models.CharField(max_length=128)
    telephone = models.CharField(max_length=15)

class Restaurant(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=80)
    menu = DictField()
