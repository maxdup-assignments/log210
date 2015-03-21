# -*- coding: utf-8 -*-
from api.models import Restaurant, User, Commande
from api.serializers import CommandeSerializer, RestaurantSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import smtplib

from django.http import HttpResponse,  HttpResponseForbidden
from rest_framework.renderers import JSONRenderer
import json

@api_view(['GET','POST','PUT'])
def commande(request, pk=None):

    if pk:
        commande = Commande.objects.get(pk=pk)

    if request.method == 'GET':

        # returns a single commande
        if pk:
            output = CommandeSerializer(commande)

        # returns commandes coresponding to resto
        elif 'resto' in request.GET:
            resto = Restaurant.objects.get(pk=request.GET['resto'])
            commandes = Commande.objects.filter(restaurant=resto)
            output = CommandeSerializer(commandes, many=True)

        # returns all commandes
        else:
            commandes = Commande.objects.all()
            output = CommandeSerializer(commandes, many=True)

        return Response(output.data)

    elif request.method == 'POST':

        # creates a commande
        resto = Restaurant.objects.get(pk=request.data.pop('resto'))
        commande = Commande(
            restaurant=resto,
            details=request.data['details'],
            status='pending')
        commande.save()
        commande = CommandeSerializer(commande)
        return Response(commande.data,
                        status=status.HTTP_201_CREATED)

    elif request.method == 'PUT':

        #udpates a commande
        request.data.pop('restaurant')
        commande = CommandeSerializer(commande, data=request.data,
                                      partial=True)
        if commande.is_valid():
            commande.save()
            return Response(commande.data)
        return Response(commande.errors, status=status.HTTP_400_BAD_REQUEST)

def send_mail(commande_info, request):
    # secure I know
    username = 'log210restaurant@gmail.com'
    password = 'log210resto'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Votre Commande"
    msg['From'] = username
    msg['To'] = request.user.username

    html = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><body><h1>Votre commande a bien ete recu</h1>
    <table>
    <tr><th>plat</th><th>prix</th><th>quantite</th></tr>'''
    for item in commande_info['details']['commande']:
        html+= '<tr><td>'+item['name']+'</td><td>'+str(item['price'])+'$</td><td>'+str(item['qty'])+'</td></tr>'
    html+="</table><br/><br/>a l'adresse: " + commande_info['details']['addressTo'] + '<br/> pour le: ' + commande_info['details']['requestedTime']+'</body></html>'

    msg.attach(MIMEText(html, 'html'))


    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(username, request.user.username, msg.as_string())
    server.quit()
    return html


def populate_commande(request):
    restaurant = Restaurant.objects.get(name='Pataterie')
    restaurant2 = Restaurant.objects.get(name='Subway')
    Commande.objects.create(
        restaurant=restaurant,
        details={
            'commande': [{
                'desc':'des patates',
                'name':'patate',
                'price':'3',
                'qty':'1'}],
            'addressTo': 'XX_destination',
            'addressFrom': 'XX_adresse_resto',
            'requestedTime': "2015-03-18T20:15:02.449Z",
        },
        status='paid')
    Commande.objects.create(
        restaurant=restaurant,
        details={
            'commande': [{
                'name': 'poutine',
                'desc': 'de la poutine',
                'price': '7',
                'qty':'1'}],
            'addressTo': 'XX_destination',
            'addressFrom': 'XX_adresse_resto',
            'requestedTime': "2015-03-18T20:15:02.449Z",
        },
        status='paid')
    Commande.objects.create(
        restaurant=restaurant2,
        details={
            'commande': [{
                'name': 'sous-marin',
                'desc': '12 pouces',
                'price': '5',
                'qty':'1'}],
            'addressTo': 'XX_destination',
            'addressFrom': 'XX_adresse_resto',
            'requestedTime': "2015-03-18T20:15:02.449Z",
        },
        status='paid')
    return HttpResponse({'success': True})
