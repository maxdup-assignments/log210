from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from api.models import UserProfile
from django.contrib.auth.models import User

from api.serializers import ProfileSerializer, UserSerializer
from rest_framework.renderers import JSONRenderer
import json

def get_current_profile(request):
    if not request.user:
        return HttpResponse({})

    user = User.objects.get(pk=request.user.pk)
    profile = UserProfile.objects.get(user=user.pk)
    profile = ProfileSerializer(profile)
    return HttpResponse(JSONRenderer().render(profile.data))

def get_profiles(request):
    #todo check auth
    users = UserProfile.objects.all()
    profiles = {'users':[]}
    for user in users:
        profile = ProfileSerializer(user)
        profiles['users'].append(profile.data)
    return HttpResponse(JSONRenderer().render(profiles))

def edit_profile(request):
    #todo check auth
    if request.method == 'POST':
        userinfo = json.loads(request.body)

        user = User.objects.get(pk=userinfo['user']['pk'])
        user.first_name = userinfo['user']['first_name']
        user.last_name = userinfo['user']['last_name']
        user.username = userinfo['user']['email']
        user.email = userinfo['user']['email']
        user.is_superuser = userinfo['user']['is_superuser']
        user.is_staff = userinfo['user']['is_staff']
        user.save()

        profile = UserProfile.objects.get(pk=userinfo['pk'])
        profile.adresse = userinfo['adresse']
        profile.telephone = userinfo['telephone']
        profile.date_naissance = userinfo['date_naissance']
        profile.save()

    return HttpResponse(json.dumps(userinfo))


def register(request):
    registered = False

    if request.method == 'POST':
        userinfo = json.loads(request.body)
        print userinfo
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

def user_login(request):
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
    logout(request)
    return HttpResponse(json.dumps({'success':True}))
