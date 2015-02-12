from django.conf.urls import patterns, url
from api.views import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register, name='register'),
    url(r'^login', views.user_login, name='login'),
    url(r'^logout', views.user_logout, name='logout'),
    url(r'^all_staff', views.get_staff, name='get_staff'),
    url(r'^profile', views.get_current_profile, name='get_current_profile'),
    url(r'^all_profiles', views.get_profiles, name='get_profiles'),
    url(r'^edit_profile', views.edit_profile, name='edit_profile'),
    url(r'^delete_profile', views.delete_profile, name='delete_profile'),
    url(r'^populateuser', views.populateUser, name='populateUser'),
    url(r'^create_resto', views.create_resto, name='create_resto'),
    url(r'^delete_resto', views.delete_resto, name='delete_resto'),
    url(r'^edit_resto', views.edit_resto, name='edit_resto'),
    url(r'^all_resto', views.all_resto, name='all_resto'),
    url(r'^assigned_resto', views.assigned_resto, name='assigned_resto'),
    url(r'^edit_menu', views.edit_menu, name='edit_menu'),
    url(r'^populateresto', views.populate_resto, name='populateresto'),
)
