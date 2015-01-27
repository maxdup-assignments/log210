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

def populateUser(request):
	user = User.objects.create_superuser(
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
	
	#if not User.objects.get(username='jacques@hotmail.com'):
	user = User.objects.create_superuser(
				username= 'jacques@hotmail.com',
	                        first_name='jacques',
	                        last_name='gabriel',            					email='jacques@hotmail.com',
				password='potato')		
	user.is_staff = True
	user.save()

	profile = UserProfile.objects.create(
	    user=user,
	    date_naissance='28 mars 2000',
	    adresse='8888 lacordaire',
	    telephone='1234567514')
	profile.save()

	#if not User.objects.get(username='maxime@hotmail.com'):
	user = User.objects.create_superuser(
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

	#if not User.objects.get(username='philippe@hotmail.com'):
	user = User.objects.create_superuser(
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
