from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse,  HttpResponseForbidden

from django.contrib.auth.models import User
from api.models import UserProfile

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
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    users = UserProfile.objects.all()
    profiles = {'users':[]}
    for user in users:
        profile = ProfileSerializer(user)
        profiles['users'].append(profile.data)
    return HttpResponse(JSONRenderer().render(profiles))

def get_staff(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    staff = User.objects.filter(is_staff=True)
    profiles = {'staff':[]}
    for user in staff:
        profile = UserSerializer(user)
        profiles['staff'].append(profile.data)
    return HttpResponse(JSONRenderer().render(profiles))

def edit_profile(request):

    if request.method == 'POST':
        userinfo = json.loads(request.body)
        if request.user.pk != userinfo['user']['pk']:
            if not request.user.is_superuser:
                return HttpResponseForbidden()

        del userinfo['backup']

        user = User.objects.get(pk=userinfo['user']['pk'])
        #magic that updates user fields from json dict
        user.__dict__.update(**userinfo['user'])
        user.save()
        del userinfo['user']

        profile = UserProfile.objects.get(pk=userinfo['pk'])
        profile.__dict__.update(**userinfo)
        profile.save()

    return HttpResponse(json.dumps({'success': True}))


def register(request):
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
