from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from api.models import UserProfile, Restaurant
from api.serializers import ProfileSerializer, UserSerializer

from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# plan to delete
from django.http import HttpResponse,  HttpResponseForbidden
from rest_framework.renderers import JSONRenderer
import json

@ensure_csrf_cookie
@api_view(['GET','POST','PUT'])
def profile(request, pk=None):

    if request.method == 'GET':
        if pk:
            user = User.objects.get(pk=request.user.pk)
            profile = UserProfile.objects.get(user=user)
            output = ProfileSerializer(profile)
        else:
            profiles = UserProfile.objects.all()
            output = ProfileSerializer(profiles, many=True)
        return Response(output.data)

    elif request.method == 'POST':
        request.data['user']['username'] = request.data['user']['email']
        profile = ProfileSerializer(data=request.data)
        if profile.is_valid():
            profile.save()
            return Response(profile.data,
                            status=status.HTTP_201_CREATED)
        return Response(profile.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        userdata = request.data.pop('user')
        user = User.objects.get(pk=request.user.pk)
        user = UserSerializer(user, data=userdata)
        if user.is_valid():
            user.save()
            profile = UserProfile.objects.get(user=user.data['pk'])
            profile = ProfileSerializer(profile, data=request.data, partial=True)
            if profile.is_valid():
                profile.save()
                print('profile saved')
                return Response(user.data)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

@ensure_csrf_cookie
def get_current_profile(request):
    # returns the current profile
    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.pk)
        profile = UserProfile.objects.get(user=user.pk)
        profile = ProfileSerializer(profile)
        return HttpResponse(JSONRenderer().render(profile.data))
    return HttpResponse()

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
    staff_request = UserProfile.objects.filter(is_restaurateur=True)
    staffs = []
    for profile in staff_request:
        staff = UserSerializer(profile.user)
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
            profile = UserProfile.objects.get(user=user)
            profile = ProfileSerializer(profile)
            return HttpResponse(json.dumps({'success':True,
                                            'profile': profile.data}))

        else:
            return HttpResponse(json.dumps({'success':False,
                                            'reason': 'fail'}))

    else:
        return HttpResponse(json.dumps({'success':False}))

def user_logout(request):
    # this is the logout request
    logout(request)
    return HttpResponse(json.dumps({'success':True}))
