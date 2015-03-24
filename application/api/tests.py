from unittest import TestCase
from django.test import Client
from pymongo import Connection
import datetime

from django.contrib.auth.models import User
from api.models import UserProfile, Restaurant, Commande
from api.serializers import ProfileSerializer, UserSerializer, RestaurantSerializer, CommandeSerializer
from api.data_population import populate_database

from api.views.account import *
from api.views.restaurant import *
from api.views.commande import *
from json import JSONEncoder

class PopulateTestCase(TestCase):
    def setUp(self):
        populate_database()

    # tests population
    def test_account_population(self):
        self.assertEqual(9, User.objects.all().count())

    def test_resto_population(self):
        self.assertEqual(4, Restaurant.objects.all().count())

    def test_commande_population(self):
        self.assertEqual(3, Commande.objects.all().count())

    #tests utilisateurs
    def test_account_login(self):
        c = Client()
        response = c.post('/api/login/', content_type='application/json',
                          data=json.dumps({'username': 'mdupuis@hotmail.ca',
                                           'password': 'asd'}))
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertTrue(body['success'])

    def test_account_logout(self):
        c = Client()
        response = c.get('/api/logout/')
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertTrue(body['success'])

    def test_account_profile(self):
        c = Client()
        c.post('/api/login/', content_type='application/json',
               data=json.dumps({'username': 'mdupuis@hotmail.ca',
                                'password': 'asd'}))

        response = c.get('/api/profile/self')
        self.assertEqual(str(response.data['user']['email']),
                         'mdupuis@hotmail.ca')
        self.assertEqual(response.status_code, 200)

    def test_account_all_profiles(self):
        c = Client()
        response = c.get('/api/profile')
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(len(body), 9)

    def test_account_all_staff(self):
        c = Client()
        response = c.get('/api/profile', {'restaurateur':'true'})
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(len(body), 4)

    def test_account_edit_profile(self):
        c = Client()
        user = User.objects.get(email='client@resto.com')
        profile = UserProfile.objects.get(user=user)
        profile.user.first_name = 'pat'
        profile.telephone = '1234567'
        request = ProfileSerializer(profile).data

        response = c.put('/api/profile', content_type='application/json',
                          data=json.dumps(request))
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body['user']['first_name'], 'pat')
        self.assertEqual(body['telephone'], '1234567')

    def test_account_delete_profile(self):
        c = Client()
        user = User.objects.get(username='jacques@hotmail.com')
        u_pk = user.pk
        profile = UserProfile.objects.get(user=user)
        pk = profile.pk
        p_pk = profile.pk
        request = UserSerializer(user).data

        response = c.delete('/api/profile/'+request['pk'],
                            content_type='application/json',
                            data=json.dumps(request))

        self.assertEqual(response.status_code, 204)
        profile = UserProfile.objects.filter(pk=p_pk).exists()
        self.assertEqual(profile, False)
        user = User.objects.filter(pk=u_pk).exists()
        self.assertEqual(user, False)

    def test_account_register(self):
        c = Client()
        userform = {
            'user':{
                'email':'asdf@asdf.com',
                'first_name':'patr',
                'last_name':'asd',
                'password':'asd'},
            'date_naissance':'asd',
            'adresse':'asd',
            'telephone':'1234',
            'is_restaurateur': False}
        response = c.post('/api/profile', content_type='application/json',
                          data=json.dumps(userform))
        self.assertEqual(response.status_code, 201)
        body = json.loads(response.content)
        self.assertEqual(body['user']['first_name'], 'patr')
        self.assertEqual(body['telephone'], '1234')
    '''

    # tests restaurant
    def test_create_resto(self):
        c = Client()
        user = User.objects.get(email='restaurateur@resto.com')
        restoform = {
            'name': 'rETSo',
            'menu': {},
            'user': user.pk,
            'address': 'some adress'
        }
        response = c.post('/api/create_resto/', content_type='application/json',
                          data=JSONRenderer().render(restoform))
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body['name'], 'rETSo')
        self.assertEqual(body['user']['pk'], user.pk)

    def test_delete_resto(self):
        c = Client()
        resto = Restaurant.objects.get(name="Buffet")
        resto = RestaurantSerializer(resto).data
        response = c.post('/api/delete_resto/',
                          content_type='application/json',
                          data=JSONRenderer().render(resto))

        self.assertEqual(response.status_code, 200)
        exist = Restaurant.objects.filter(pk=resto['pk']).exists()
        self.assertEqual(exist, False)

    def test_all_resto(self):
        c = Client()
        response = c.get('/api/all_resto/')
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(len(body), 4)

    def test_assigned_resto(self):
        c = Client()
        c.post('/api/login/', content_type='application/json',
               data=json.dumps({'username': 'andy@hotmail.com',
                                'password': 'patate'}))
        response = c.get('/api/assigned_resto/')
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(len(body), 1)

    def test_edit_resto(self):
        c = Client()
        resto = Restaurant.objects.get(name="Buffet")

        resto.name = 'Le Buffet'
        resto.address = 'newaddress'
        request = RestaurantSerializer(resto).data

        response = c.post('/api/edit_resto/', content_type='application/json',
                          data=JSONRenderer().render(request))
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body['name'], 'Le Buffet')
        self.assertEqual(body['address'], 'newaddress')

    # tests commandes
    def test_create_commande(self):
        c = Client()
        resto = Restaurant.objects.get(name="Pataterie")
        c.post('/api/login/', content_type='application/json',
               data=json.dumps({'username': 'mdupuis@hotmail.ca',
                                'password': 'asd'}))
        order = {
            'details': {
                'commande': [{
                    'desc':'des patates',
                    'name':'patate',
                    'price':'3',
                    'qty':'1'}],
                'addressTo': 'XX_destination',
                'addressFrom': 'XX_adresse_resto',
                'requestedTime': datetime.datetime.now(),
            },
            'restaurant': resto.pk
        }

        response = c.post('/api/create_commande/', content_type='application/json',
                          data=JSONRenderer().render(order))
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body['details']['addressTo'], 'XX_destination')
        self.assertEqual(body['restaurant']['pk'], resto.pk)

    def test_get_commande(self):
        c = Client()
        commande = Commande.objects.all()[0]
        response = c.post('/api/get_commande/', content_type='application/json',
               data=commande.pk)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body['status'], 'paid')

    def test_resto_commande(self):
        c = Client()
        resto = Restaurant.objects.get(name="Pataterie")
        commande = Commande.objects.filter(restaurant=resto)
        response = c.post('/api/resto_commande/',
                          content_type='application/json', data=resto.pk)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(2, len(body))

    def test_update_commande(self):
        c = Client()
        commande = Commande.objects.all()[0]
        response = c.post('/api/update_commande/',
                          content_type='application/json',
                          data=json.dumps({'status':'preparing',
                                           'commande':CommandeSerializer(commande).data}))
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual('preparing', body['status'])

    '''

    def tearDown(self):
        c = Connection()
        c.drop_database('test_resto')
