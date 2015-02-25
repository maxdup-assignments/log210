from django.http import HttpResponse,  HttpResponseForbidden

from api.models import Restaurant, User, Commande

from api.serializers import CommandeSerializer
from rest_framework.renderers import JSONRenderer
import json


def create_commande(request):
    commande_info = json.loads(request.body)
    restaurant = Restaurant.objects.get(pk=commande_info['restaurant'])
    commande = Commande.objects.create(
        user=request.user,
        restaurant=restaurant,
        details=commande_info['details'],
        status='pending')

    commande.save()
    commande = CommandeSerializer(commande)
    return HttpResponse(JSONRenderer().render(commande.data))

def resto_commande(request):
    resto = Restaurant.objects.get(pk=request.body)
    commandes = Commande.objects.filter(restaurant=resto)
    response = []
    for commande in commandes:
        commande = CommandeSerializer(commande)
        response.append(commande.data)
    return HttpResponse(JSONRenderer().render(response))

def update_commande_status(request):
    commande_info = json.loads(request.body)
    commande = Commande.objects.get(pk=commande_info['commande']['pk'])
    commande.status = commande_info['status']

    commande.save()
    commande = CommandeSerializer(commande)
    return HttpResponse(JSONRenderer().render(commande.data))
