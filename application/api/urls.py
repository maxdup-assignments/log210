from django.conf.urls import patterns, url
from api.views import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register, name='register'),
    url(r'^login', views.user_login, name='login'),
    url(r'^logout', views.user_logout, name='logout'),
    url(r'^profile', views.get_profile, name='get_profile'),
    url(r'^edit_profile', views.edit_profile, name='edit_profile')
)
