from unittest import TestCase
from django.test import Client
from pymongo import Connection

from django.contrib.auth.models import User
from api.models import UserProfile, Restaurant, Commande
from api.serializers import ProfileSerializer, UserSerializer

from api.views.account import *
from json import JSONEncoder

class PopulateTestCase(TestCase):
    def setUp(self):
        populateUser(None)

    def test_account_population(self):
        admin = User.objects.get(username="admin@resto.com")
        self.assertEqual(admin.first_name, 'admin')
        self.assertEqual(1,1)

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
        response = c.get('/api/profile/')
        self.assertEqual(response.status_code, 200)

    def test_account_all_profiles(self):
        c = Client()
        response = c.get('/api/all_profiles/')
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(len(body), 9)

    def test_account_all_staff(self):
        c = Client()
        response = c.get('/api/all_staff/')
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

        response = c.post('/api/edit_profile/', content_type='application/json',
                          data=JSONRenderer().render(request))
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertTrue(body['success'])

    def test_account_delete_profile(self):
        c = Client()
        user = User.objects.get(email='jacques@hotmail.com')
        profile = UserProfile.objects.get(user=user)
        pk = profile.pk
        request = ProfileSerializer(profile).data

        response = c.post('/api/delete_profile/', content_type='application/json',
                          data=JSONRenderer().render(request))

        self.assertEqual(response.status_code, 200)
        profile = UserProfile.objects.filter(pk=pk).exists()
        self.assertEqual(profile, False)

    def test_account_register(self):
        c = Client()
        userform = {'email':'asd',
                    'first_name':'patr',
                    'last_name':'asd',
                    'date_naissance':'asd',
                    'adresse':'asd',
                    'telephone':'1234',
                    'password':'asd',
                    'is_restaurateur': False}
        response = c.post('/api/register/', content_type='application/json',
                          data=JSONRenderer().render(userform))
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body['user']['first_name'], 'patr')
        self.assertEqual(body['telephone'], '1234')

    def tearDown(self):
        c = Connection()
        c.drop_database('test_resto')
