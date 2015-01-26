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
