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
from twilio.rest import TwilioRestClient
from api.config import *


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
        resto = Restaurant.objects.get(pk=request.data.pop('restaurant'))
        commande = Commande(
            restaurant=resto,
            details=request.data['details'],
            status='pending')
        commande.save()
        commande = CommandeSerializer(commande).data
        send_mail(commande, request)
        return Response(commande,
                        status=status.HTTP_201_CREATED)

    elif request.method == 'PUT':

        #udpates a commande
        request.data.pop('restaurant')
        commande = CommandeSerializer(commande, data=request.data,
                                      partial=True)
        if commande.is_valid():
            commande.save()
            commande = commande.data
            if commande['details']['notify']:
                send_sms(commande)
            return Response(commande)
        return Response(commande.errors, status=status.HTTP_400_BAD_REQUEST)

def send_sms(commande_info):
    if not (sender_sms and ACCOUNT_SID and AUTH_TOKEN):
        return
    if commande_info['status'] == 'preparing':
        body = "Votre commande est en préparation"
    else:
        body = "Votre commande est prete à être livré"
    '''
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        to=commande_info['details']['notify'],
        from_=sender_sms,
        body=body,
    )'''
    print sender_sms
    print commande_info['details']['notify']
    print body

def send_mail(commande_info, request):
    if not(sender_email and password_email):
       return
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Votre Commande"
    msg['From'] = sender_email
    msg['To'] = request.user.username
    total = 0

    html = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><body><h1>Votre commande a bien ete recu</h1>
    <table>
    <tr><th>plat</th><th>prix</th><th>quantite</th></tr>'''
    for item in commande_info['details']['commande']:
        html+= '<tr><td>'+item['name']+'</td><td>'+str(item['price'])+'$</td><td>'+str(item['qty'])+'</td></tr>'
        total+= int(item['price'])
    html+="</table><br/><br/>total: "+str(total)+"$<br/>a l'adresse: " + commande_info['details']['addressTo'] + '<br/> pour le: ' + commande_info['details']['requestedTime']+'</body></html>'

    msg.attach(MIMEText(html, 'html'))

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(sender_email, password_email)
    server.sendmail(sender_email, request.user.username, msg.as_string())
    server.quit()
    return html
