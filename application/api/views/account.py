from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,  HttpResponseForbidden

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from permission_backend_nonrel import utils

from api.models import UserProfile, Restaurant

from api.serializers import ProfileSerializer, UserSerializer
from rest_framework.renderers import JSONRenderer
import json

def get_current_profile(request):
    # returns the current profile
    if not request.user.pk:
        return HttpResponseForbidden()

    user = User.objects.get(pk=request.user.pk)
    profile = UserProfile.objects.get(user=user.pk)
    profile = ProfileSerializer(profile)
    return HttpResponse(JSONRenderer().render(profile.data))

def get_profiles(request):
    # returns all profiles
    users = UserProfile.objects.all()
    profiles = []
    for user in users:
        profile = ProfileSerializer(user)
        profiles.append(profile.data)
    return HttpResponse(JSONRenderer().render(profiles))

def delete_profile(request):
    # deletes a profile in database
    userinfo = json.loads(request.body)

    profile = UserProfile.objects.get(pk=userinfo['pk'])
    profile.delete()
    user = User.objects.get(pk=userinfo['user']['pk'])
    resto = Restaurant.objects.filter(user=user).update(user=None)
    user.delete()

    return HttpResponse({'success': True})

def get_staff(request):
    # returns all staff users
    staff_request = User.objects.filter(is_staff=True)
    staffs = []
    for user in staff_request:
        staff = UserSerializer(user)
        staffs.append(staff.data)

    return HttpResponse(JSONRenderer().render(staffs))

def edit_profile(request):
    # updates profile informations
    if request.method == 'POST':
        userinfo = json.loads(request.body)

        if 'backup' in userinfo:
            del userinfo['backup']

        user = User.objects.get(pk=userinfo['user']['pk'])
        #magic that updates user fields from json dict
        user.__dict__.update(**userinfo['user'])
        if 'password' in userinfo and userinfo['password']:
            user.set_password(userinfo['password'])
        user.email = user.username
        user.save()
        del userinfo['user']

        profile = UserProfile.objects.get(pk=userinfo['pk'])
        profile.__dict__.update(**userinfo)
        profile.save()

    return HttpResponse(json.dumps({'success': True}))

def register(request):
    # creates a new Profile

    if request.method == 'POST':
        userinfo = json.loads(request.body)
        user = User.objects.create_user(username=userinfo['email'],
                                        first_name=userinfo['first_name'],
                                        last_name=userinfo['last_name'],
                                        email=userinfo['email'],)
        user.set_password(userinfo['password'])
        user.save()
        profile = UserProfile.objects.create(
            user=user,
            date_naissance=userinfo['date_naissance'],
            adresse=[userinfo['adresse']],
            telephone=userinfo['telephone'],
            is_restaurateur=userinfo['is_restaurateur']
)
        profile.save()
        profile = ProfileSerializer(profile)

        if 'resto' in userinfo:
            if userinfo['resto']:
                resto = Restaurant.objects.filter(pk=userinfo['resto'])[0]
                resto.user = user
                resto.save()

        return HttpResponse(JSONRenderer().render(profile.data))
    return HttpResponse(json.dumps({}))

def user_login(request):
    # this is the login request
    if request.method == 'POST':
        info = json.loads(request.body)
        user = authenticate(username=info['username'],
                            password=info['password'])
        if user:
            login(request, user)
            return HttpResponse(json.dumps({'success':True,
                                            'username':user.email}))

        else:
            return HttpResponse(json.dumps({'success':False,
                                            'reason': 'fail'}))

    else:
        return HttpResponse(json.dumps({'success':False}))

def user_logout(request):
    # this is the logout request
    logout(request)
    return HttpResponse(json.dumps({'success':True}))

def populateUser(request):
    # script that will populate the database with users
    
    if not User.objects.filter(username='admin@resto.com').exists():
        user = User.objects.create_user(
            username='admin@resto.com',
            first_name='admin',
            last_name='f',
            email='admin@resto.com',
            password='asd')
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='24 mars 2010',
            adresse=['8907 14e avenue'],
            telephone='5148800928',
            is_admin=True)
        profile.save()

    if not User.objects.filter(username='entrepreneur@resto.com').exists():
        user = User.objects.create_user(
            username='entrepreneur@resto.com',
            first_name='entrepreneur',
            last_name='f',
            email='entrepreneur@resto.com',
            password='asd')
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='24 mars 2010',
            adresse=['8907 14e avenue'],
            telephone='5148800928',
            is_entrepreneur=True)
        profile.save()

    if not User.objects.filter(username='restaurateur@resto.com').exists():
        user = User.objects.create_user(
            username='restaurateur@resto.com',
            first_name='restaurateur',
            last_name='f',
            email='restaurateur@resto.com',
            password='asd')
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='24 mars 2010',
            adresse=['8907 14e avenue'],
            telephone='5148800928',
            is_restaurateur=True)
        profile.save()

    if not User.objects.filter(username='livreur@resto.com').exists():
        user = User.objects.create_user(
            username='livreur@resto.com',
            first_name='livreur',
            last_name='f',
            email='restaurateur@resto.com',
            password='asd')
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='24 mars 2010',
            adresse=['8907 14e avenue'],
            telephone='5148800928',
            is_livreur=True)
        profile.save()

    if not User.objects.filter(username='andy@hotmail.com').exists():
        user = User.objects.create_user(
            username='andy@hotmail.com',
            first_name='Andy',
            last_name='Su',
            email='andy@hotmail.com',
            password='patate')
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='26 mars 2010',
            adresse=['8907 14e avecu'],
            telephone='5148800928')
        profile.save()

    if not User.objects.filter(username='jacques@hotmail.com').exists():
        user = User.objects.create_user(
            username= 'jacques@hotmail.com',
            first_name='jacques',
            last_name='gabriel',
            email='jacques@hotmail.com',
            password='potato')
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='28 mars 2000',
            adresse=['8888 lacordaire'],
            telephone='1234567514')
        profile.save()

    if not User.objects.filter(username='mdupuis@hotmail.ca').exists():
        user = User.objects.create_user(
            username= 'mdupuis@hotmail.ca',
            first_name='maxime',
            last_name='dupuis',
            email='mdupui@hotmail.ca',
            password='asd')
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='27 mars 1990',
            adresse=['8212 dumoulin'],
            telephone='1234561234')
        profile.save()

    if not User.objects.filter(username='philippe@hotmail.com').exists():
        user = User.objects.create_user(
            username= 'philippe@hotmail.com',
            first_name='philippe',
            last_name='murray',
            email='philippe@hotmail.com',
            password='potate')
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='25 mars 1980',
            adresse=['8210 dumouton'],
            telephone='5432102020')
        profile.save()

    return HttpResponse(json.dumps({'success':True}))
