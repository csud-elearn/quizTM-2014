from django.conf.urls import patterns, include, url
from common.views import *


urlpatterns = patterns('',
    url(r'^register/$', register, name='register'),
    url(r'^login/$', connexion, name='connexion'),
    url(r'^logout/$', deconnexion, name='deconnexion'),
)