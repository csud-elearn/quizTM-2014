from django.conf.urls import patterns, include, url
from permission.views import *


urlpatterns = patterns('',
    url(r'^home/$', home, name="home"),
    url(r'^teachers/$', teachers, name="teachers"),
    url(r'^teachers2/$', teachers, name="teachers2"),
    url(r'^students/$', students, name="students"),
)