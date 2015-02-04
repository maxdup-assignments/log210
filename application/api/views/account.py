from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,  HttpResponseForbidden

from django.contrib.auth.models import User
from api.models import UserProfile

from api.serializers import ProfileSerializer, UserSerializer
from rest_framework.renderers import JSONRenderer
import json

def get_current_profile(request):
    # returns the current profile
    if not request.user:
        return HttpResponseForbidden()

    user = User.objects.get(pk=request.user.pk)
    profile = UserProfile.objects.get(user=user.pk)
    profile = ProfileSerializer(profile)
    return HttpResponse(JSONRenderer().render(profile.data))

def get_profiles(request):
    # returns all profiles
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    users = UserProfile.objects.all()
    profiles = []
    for user in users:
        profile = ProfileSerializer(user)
        profiles.append(profile.data)
    return HttpResponse(JSONRenderer().render(profiles))

def get_staff(request):
    # returns all staff users
    if not request.user.is_superuser:
        return HttpResponseForbidden()

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
        if request.user.pk != userinfo['user']['pk']:
            if not request.user.is_superuser:
                return HttpResponseForbidden()

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
    registered = False

    if request.method == 'POST':
        userinfo = json.loads(request.body)
        user = User.objects.create_user(username=userinfo['email'],
                                        first_name=userinfo['first_name'],
                                        last_name=userinfo['last_name'],
                                        email=userinfo['email'])
        user.set_password(userinfo['password'])
        user.save()
        profile = UserProfile.objects.create(
            user=user,
            date_naissance=userinfo['date_naissance'],
            adresse=userinfo['adresse'],
            telephone=userinfo['telephone'])
        profile.save()

        return HttpResponse(json.dumps({'success':True}))
    return HttpResponse(json.dumps({'success':False}))

def populateUser(request):

    if not User.objects.filter(username='asd@asd.com').exists():
        user = User.objects.create_superuser(
            username='asd@asd.com',
            first_name='Asd',
            last_name='f',
            email='asd@asd.com',
            password='asd')
        user.is_staff = True
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='24 mars 2010',
            adresse='8907 14e avecu',
            telephone='5148800928')
        profile.save()

    if not User.objects.filter(username='asdf@asdf.com').exists():
        user = User.objects.create_user(
            username='asdf@asdf.com',
            first_name='Asdf',
            last_name='g',
            email='asdf@asdf.com',
            password='asd')
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='25 mars 2010',
            adresse='8907 14e avecu',
            telephone='5148800928')
        profile.save()

    if not User.objects.filter(username='andy@hotmail.com').exists():
        user = User.objects.create_user(
            username='andy@hotmail.com',
            first_name='Andy',
            last_name='Su',
            email='andy@hotmail.com',
            password='patate')
        user.is_staff = True
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='26 mars 2010',
            adresse='8907 14e avecu',
            telephone='5148800928')
        profile.save()

    if not User.objects.filter(username='jacques@hotmail.com').exists():
        user = User.objects.create_user(
            username= 'jacques@hotmail.com',
            first_name='jacques',
            last_name='gabriel',
            email='jacques@hotmail.com',
            password='potato')
        user.is_staff = True
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='28 mars 2000',
            adresse='8888 lacordaire',
            telephone='1234567514')
        profile.save()

    if not User.objects.filter(username='maxime@hotmail.com').exists():
        user = User.objects.create_user(
            username= 'maxime@hotmail.com',
            first_name='maxime',
            last_name='dupuis',
            email='maxime@hotmail.com',
            password='patato')
        user.is_staff = True
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='27 mars 1990',
            adresse='8212 dumoulin',
            telephone='1234561234')
        profile.save()

    if not User.objects.filter(username='philippe@hotmail.com').exists():
        user = User.objects.create_user(
            username= 'philippe@hotmail.com',
            first_name='philippe',
            last_name='murray',
            email='philippe@hotmail.com',
            password='potate')
        user.is_staff = True
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            date_naissance='25 mars 1980',
            adresse='8210 dumouton',
            telephone='5432102020')
        profile.save()

    return HttpResponse(json.dumps({'success':True}))

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
