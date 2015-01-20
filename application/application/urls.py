from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from resto import frontend
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = patterns('',
    url(r'^$', frontend.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
)
