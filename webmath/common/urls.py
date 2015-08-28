from django.conf.urls import patterns, include, url
from common.views import *


urlpatterns = patterns('',
    url(r'^register/student$', register_student, name='register_student'),
    # url(r'^register/teacher$', register_teacher, name='register_teacher'),
    url(r'^login/$', connexion, name='connexion'),
    url(r'^logout/$', deconnexion, name='deconnexion'),
)