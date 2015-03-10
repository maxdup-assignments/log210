# -*- coding: utf-8 -*-
from django.http import HttpResponse,  HttpResponseForbidden

from api.models import Restaurant, User, Commande

from api.serializers import CommandeSerializer
from rest_framework.renderers import JSONRenderer
import json

import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_commande(request):
    commande_info = json.loads(request.body)

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

    restaurant = Restaurant.objects.get(pk=commande_info['restaurant'])
    commande = Commande.objects.create(
        user=request.user,
        restaurant=restaurant,
        details=commande_info['details'],
        status='paid')

    send_mail(commande_info, request)

    commande.save()
    commande = CommandeSerializer(commande)
    return HttpResponse(JSONRenderer().render(commande.data))

def get_commande(request):
    commande = Commande.objects.get(pk=request.body)
    response = CommandeSerializer(commande).data
    return HttpResponse(JSONRenderer().render(response))

def resto_commande(request):
    if request.body:
        resto = Restaurant.objects.get(pk=request.body)
        commandes = Commande.objects.filter(restaurant=resto)
    else:
        commandes = Commande.objects.all()
    response = []
    for commande in commandes:
        commande = CommandeSerializer(commande)
        response.append(commande.data)
    return HttpResponse(JSONRenderer().render(response))

def update_commande_status(request):
    commande_info = json.loads(request.body)
    commande = Commande.objects.get(pk=commande_info['commande']['pk'])
    note = {}

    if commande_info['status'] == 'delivered':
        if commande.status == 'delivered':
            note['error'] = 'already delivered'
        else:
            commande.details['deliveryTime'] = datetime.datetime.now()

    if commande_info['status'] == 'paid':
        if commande.status == 'pending':
            commande.status = commande_info['status']
    else:
        commande.status = commande_info['status']

    commande.save()
    response = CommandeSerializer(commande).data
    if note:
        response.update(note)
    return HttpResponse(JSONRenderer().render(response))
